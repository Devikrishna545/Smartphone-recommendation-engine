"""Google ADK entry point and chat helper for the smartphone recommendation agent."""

import uuid

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .tools import compare_smartphones, recommend_smartphones, review_smartphone

root_agent = Agent(
    name="smartphone_data_analyst",
    model="gemini-2.5-flash",
    description="Answers questions about the bundled smartphone specifications dataset.",
    instruction=(
        "You are an expert smartphone recommendation analyst. Use the provided tools for "
        "factual questions about smartphone reviews, comparisons, prices, ratings, and 5G "
        "capabilities. State clearly when the dataset has no matching result. Do not invent "
        "device specifications or prices."
    ),
    tools=[review_smartphone, compare_smartphones, recommend_smartphones],
)

APP_NAME = "smartphone_recommendation"
_session_service = InMemorySessionService()
_runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=_session_service)
_known_sessions: set[str] = set()


async def ask_agent(message: str, session_id: str | None = None) -> tuple[str, list[str], str]:
    """Run one agent turn and return its text, tool names, and session identifier."""
    session_id = session_id or str(uuid.uuid4())
    if session_id not in _known_sessions:
        await _session_service.create_session(
            app_name=APP_NAME,
            user_id="web_user",
            session_id=session_id,
        )
        _known_sessions.add(session_id)

    reply_parts: list[str] = []
    tool_names: list[str] = []
    message_content = types.Content(role="user", parts=[types.Part(text=message)])
    async for event in _runner.run_async(
        user_id="web_user",
        session_id=session_id,
        new_message=message_content,
    ):
        for function_call in event.get_function_calls() or []:
            if function_call.name not in tool_names:
                tool_names.append(function_call.name)
        if event.is_final_response() and event.content and event.content.parts:
            reply_parts.extend(
                part.text for part in event.content.parts if getattr(part, "text", None)
            )

    reply = "\n".join(reply_parts).strip()
    return reply or "The agent returned no text.", tool_names, session_id
