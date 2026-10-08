courses = {
    "AI": {
        "time": "Monday 09:00",
        "room": "A101",
        "teacher": "王老師"
    },
    "Database": {
        "time": "Tuesday 10:00",
        "room": "B202",
        "teacher": "陳老師"
    },
    "Network": {
        "time": "Wednesday 13:00",
        "room": "C303",
        "teacher": "林老師"
    }
}


def get_course_info(course):
    return courses.get(course, "找不到這門課")


# 測試 Tool
# print(get_course_info("AI"))
