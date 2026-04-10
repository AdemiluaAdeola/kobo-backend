from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["AI Coach"])


# System prompt (same persona from the landing page)
KOBO_SYSTEM_PROMPT = """You are Kobo, an AI financial coach built specifically for young Nigerian professionals aged 22–35. You are sharp, warm, empathetic, and unpretentious — a knowledgeable friend, not a bank.

Key traits:
- You deeply understand Nigerian financial culture: black tax (supporting family), esusu (cooperative savings), aso-ebi (event clothing obligations), Detty December (festive spending season), multiple income streams, NYSC, side hustles
- You're comfortable with Pidgin English and Naija slang. Respond in Pidgin if the user does — otherwise use warm, clear English
- You NEVER shame people about their spending
- Use ₦ (Naira) for all amounts
- Responses: concise (2–3 short paragraphs), conversational, specific and actionable
- Use emojis naturally but sparingly
- You know: PiggyVest, Cowrywise, Kuda, Carbon, Palmcredit, Opay, Moniepoint, Mono, Flutterwave, Paystack
- Typical salary range: ₦150k–₦1.5M/month
- Common Nigerian expense categories: rent, transport, food, subscriptions (Netflix/DSTV/Spotify), data, clothing (aso-ebi), black tax, esusu, church/tithe, informal loans

When someone says they're broke before payday: validate it, identify the most likely cause, give 2–3 specific steps.
When asked if they can afford something: give a direct answer with a naira number.
When asked to build a budget: split into needs/wants/savings practically for Lagos life.
Be the coach that makes them move from reactive to predictive."""


def _stub_reply(message: str) -> str:
    """Rule-based stub replies (matches landing page demo logic)."""
    lower = message.lower()

    if "budget" in lower and "350" in lower:
        return (
            "Okay so ₦350k. In Lagos, try this:\n\n"
            "• ₦175k (50%) → Fixed needs: rent, transport, food, data\n"
            "• ₦105k (30%) → Wants: flex money, aso-ebi, subscriptions\n"
            "• ₦70k (20%) → Save/invest immediately on payday\n\n"
            "Would you like me to set up auto-save for the ₦70k next payday? 🎯"
        )
    if "dinner" in lower:
        return (
            "Looking at your current trajectory, you have about ₦3,400 \"safe to spend\" "
            "before your next payday. A nice dinner out is fine — but try to keep it under "
            "₦2,500 so you're not stressed next week. 🍽️"
        )
    if "25th" in lower or "run out" in lower:
        return (
            "The salary trap! 😩 It happens because we usually pay bills and flex first, then "
            "save whatever's left (which is usually nothing).\n\n"
            "Next month, let's reverse it — secure savings + fixed costs on Day 1. "
            "Try the 50/30/20 split and auto-transfer your savings the minute salary lands."
        )
    if "detty december" in lower:
        return (
            "Ah, Detty December! 🎉 The earlier you start, the less you feel it.\n\n"
            "If we auto-save ₦25,000 every month starting now, you'll have ₦200,000 "
            "ready by November — no loans, no stress."
        )
    if "emergency" in lower or "lagos" in lower:
        return (
            "For a young professional in Lagos, aim for 3–6 months of bare-minimum "
            "living expenses.\n\n"
            "If your basics cost ₦150k/month, a full emergency fund is ₦450k–₦900k. "
            "Start with ₦50k and grow it gradually — even ₦10k/month adds up. 💪"
        )
    if "subscription" in lower or "forgetting" in lower:
        return (
            "You're not alone! Common culprits: Netflix (₦4,400), Spotify (₦2,950), "
            "DSTV, Apple Music.\n\n"
            "I can send you a nudge 48 hours before each renewal so you can cancel or "
            "pause the ones you're not using. Want me to turn that on? ⚡"
        )
    if "family" in lower or "30k" in lower or "black tax" in lower:
        return (
            "Black tax is real, no shame in it. 🤝\n\n"
            "Easiest fix: treat that ₦30k like a fixed utility bill. Set up an auto-transfer "
            "to your family's account on payday. You won't even see the money, so you won't "
            "plan your life around it."
        )

    # Default reply
    return (
        "I hear you! To give you the best personalised advice, I'd need to look at your "
        "full transaction history.\n\n"
        "But generally, the #1 thing that stops the \"always broke before payday\" cycle: "
        "auto-save your target amount the second salary lands — before you spend anything. "
        "Would you like me to help you set that up? 💰"
    )


@router.post("", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Talk to the Kobo AI financial coach.
    Currently uses rule-based stub replies. Wire up OpenAI/Anthropic
    via config.AI_PROVIDER when ready.
    """
    reply = _stub_reply(data.message)
    return ChatResponse(reply=reply)
