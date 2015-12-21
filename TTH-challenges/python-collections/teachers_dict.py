teachers_dict = {'Kenneth Love': ['Python Basics', 'Python Collections'],
                 'Jason Seifer': ['Ruby Foundations', 'Ruby on Rails Forms', 'Technology Foundations']}


def most_classes(teachers_dict):
    result_disct = {}
    maxValue = 0
    for key in teachers_dict:
        if len(teachers_dict[key]) > maxValue:
            maxValue = len(teachers_dict[key])
            result_disct = {key: len(teachers_dict[key])}

    return list(result_disct.keys())[0]


def num_teachers(teachers_dict):
    teachercounter = 0
    for key in teachers_dict:
        teachercounter += 1
    return teachercounter


def most_classes(teachers_dict):
    result_disct = {}
    maxValue = 0
    for key in teachers_dict:
        if len(teachers_dict[key]) > maxValue:
            maxValue = len(teachers_dict[key])
            result_disct = {key: len(teachers_dict[key])}

    return list(result_disct.keys())[0]


def stats(x):
    teacher_list = []
    for key in x:
        teacher_list.append([key, len(x[key])])
    return teacher_list


def courses(my_dict):
    course_list = []
    for key in my_dict:
        for course in my_dict[key]:
            course_list.append(course)
    return course_list
