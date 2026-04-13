"""Date Calculator AI MCP Server — Date math tools."""
import time
from datetime import datetime, timedelta
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("date-calculator-ai-mcp")
_calls: dict[str, list[float]] = {}
DAILY_LIMIT = 50

def _rate_check(tool: str) -> bool:
    now = time.time()
    _calls.setdefault(tool, [])
    _calls[tool] = [t for t in _calls[tool] if t > now - 86400]
    if len(_calls[tool]) >= DAILY_LIMIT:
        return False
    _calls[tool].append(now)
    return True

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

@mcp.tool()
def days_between(date1: str, date2: str) -> dict[str, Any]:
    """Calculate days between two dates (YYYY-MM-DD). Also returns weeks, months estimate, and business days."""
    if not _rate_check("days_between"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    delta = d2 - d1
    days = abs(delta.days)
    # Count business days
    biz = 0
    start, end = min(d1, d2), max(d1, d2)
    current = start
    while current < end:
        if current.weekday() < 5:
            biz += 1
        current += timedelta(days=1)
    return {
        "date1": date1, "date2": date2, "days": delta.days,
        "absolute_days": days, "weeks": round(days / 7, 1),
        "business_days": biz, "weekends": days - biz,
        "months_approx": round(days / 30.44, 1), "years_approx": round(days / 365.25, 2),
        "day1_weekday": WEEKDAYS[d1.weekday()], "day2_weekday": WEEKDAYS[d2.weekday()]
    }

@mcp.tool()
def add_business_days(start_date: str, business_days: int, holidays: str = "") -> dict[str, Any]:
    """Add business days to a date, optionally excluding holidays (comma-separated YYYY-MM-DD)."""
    if not _rate_check("add_business_days"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        current = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    holiday_set = set()
    if holidays:
        for h in holidays.split(","):
            try:
                holiday_set.add(datetime.strptime(h.strip(), "%Y-%m-%d").date())
            except ValueError:
                pass
    added = 0
    direction = 1 if business_days >= 0 else -1
    target = abs(business_days)
    skipped_holidays = 0
    skipped_weekends = 0
    while added < target:
        current += timedelta(days=direction)
        if current.weekday() >= 5:
            skipped_weekends += 1
            continue
        if current.date() in holiday_set:
            skipped_holidays += 1
            continue
        added += 1
    return {
        "start_date": start_date, "business_days_added": business_days,
        "result_date": current.strftime("%Y-%m-%d"), "result_weekday": WEEKDAYS[current.weekday()],
        "calendar_days_elapsed": abs((current - datetime.strptime(start_date, "%Y-%m-%d")).days),
        "weekends_skipped": skipped_weekends, "holidays_skipped": skipped_holidays
    }

@mcp.tool()
def next_weekday(start_date: str, target_day: str, occurrence: int = 1) -> dict[str, Any]:
    """Find the next occurrence of a weekday. target_day: Monday-Sunday. occurrence: nth occurrence (1-52)."""
    if not _rate_check("next_weekday"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        current = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    day_names = {d.lower(): i for i, d in enumerate(WEEKDAYS)}
    target = day_names.get(target_day.lower())
    if target is None:
        return {"error": f"Invalid day. Use: {', '.join(WEEKDAYS)}"}
    if occurrence < 1 or occurrence > 52:
        return {"error": "Occurrence must be 1-52"}
    found = 0
    check = current
    while found < occurrence:
        check += timedelta(days=1)
        if check.weekday() == target:
            found += 1
    return {
        "start_date": start_date, "target_day": WEEKDAYS[target],
        "occurrence": occurrence, "result_date": check.strftime("%Y-%m-%d"),
        "days_from_start": (check - current).days
    }

@mcp.tool()
def format_date(date_string: str, input_format: str = "%Y-%m-%d", output_format: str = "%B %d, %Y") -> dict[str, Any]:
    """Parse and reformat dates. Common formats: %Y-%m-%d, %d/%m/%Y, %m/%d/%Y, %B %d %Y, %A %B %d %Y, %Y%m%d, ISO8601."""
    if not _rate_check("format_date"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        dt = datetime.strptime(date_string, input_format)
    except ValueError:
        return {"error": f"Cannot parse '{date_string}' with format '{input_format}'"}
    formats = {
        "ISO 8601": dt.strftime("%Y-%m-%dT%H:%M:%S"),
        "US": dt.strftime("%m/%d/%Y"),
        "EU": dt.strftime("%d/%m/%Y"),
        "Long": dt.strftime("%B %d, %Y"),
        "Full": dt.strftime("%A, %B %d, %Y"),
        "Short": dt.strftime("%b %d, %Y"),
        "Compact": dt.strftime("%Y%m%d"),
        "Unix": str(int(dt.timestamp())) if dt.year >= 1970 else "N/A",
    }
    return {
        "input": date_string, "parsed": dt.isoformat(),
        "formatted": dt.strftime(output_format), "output_format": output_format,
        "all_formats": formats, "weekday": WEEKDAYS[dt.weekday()],
        "day_of_year": dt.timetuple().tm_yday,
        "is_leap_year": dt.year % 4 == 0 and (dt.year % 100 != 0 or dt.year % 400 == 0),
        "quarter": (dt.month - 1) // 3 + 1
    }

if __name__ == "__main__":
    mcp.run()
