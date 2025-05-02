from app.utils.constants import PROMPT_TYPE, PROMPT_CATEGORY

PROMPT_MAP = {
    PROMPT_CATEGORY.ROUTINE_GENERATOR: {
        PROMPT_TYPE.SYSTEM_PROMPT: """Please generate a structured plan following this
        format for a user who is looking to improve their career, finance, relationships,
        and daily routines. Each section (career, finance, relationships, daily routine)
        should have specific actionable steps organized by time frame (daily, weekly, monthly).
        Example Output Format:
        {OUTPUT_FORMAT}

        Return only a valid JSON object that exactly follows this format with no additional text.
        """,
        PROMPT_TYPE.USER_PROMPT: """The user data is:
        {USER_DATA}
        """,
    },
    PROMPT_CATEGORY.DAILY_HABIT_GENERATOR: {
        PROMPT_TYPE.SYSTEM_PROMPT: """Please create a set of daily habits for a user
        based on their career goals, personal development, and well-being. The habits
        should focus on key areas such as productivity, health, mindset, relationships,
        and finance. Ensure the habits are realistic, actionable, and aligned with
        the user's stated goals.
        The output should provide daily habits structured by category, with clear
        time frames for each.
        Example Output Format:
        {OUTPUT_FORMAT}

        Return only a valid JSON object that exactly follows this format with no additional text.
        """,
        PROMPT_TYPE.USER_PROMPT: """The user data is:
        {USER_DATA}
        """,
    },
    PROMPT_CATEGORY.FEAR_AND_MOTIVATION_GENERATOR: {
        PROMPT_TYPE.SYSTEM_PROMPT: """Please generate a motivational framework for a
        user based on their goals and challenges. The framework should identify key fears
        or obstacles that may be preventing progress, and provide motivational strategies
        or actions to overcome them. It should also highlight the user's core motivations
        and suggest actions to maintain focus and momentum.
        The output should focus on practical steps for overcoming fear and sustaining motivation.
        Example Output Format:
        {OUTPUT_FORMAT}

        Return only a valid JSON object that exactly follows this format with no additional text.
        """,
        PROMPT_TYPE.USER_PROMPT: """The user data is:
        {USER_DATA}
        """,
    },
}
