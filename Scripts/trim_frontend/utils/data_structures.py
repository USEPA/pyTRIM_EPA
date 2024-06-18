# depth-first recursive method that drills into a list and
# tells us how deep it is.
#
# e.g. [] -> 1
#      [ [x,y] ] -> 2
#      [ [ [ x,y] ] ] -> 3
#      "foo" / None / any_non_list_obj / etc. -> 0
#
# assumes similar depth throughout list as it only checks the first element at each level.
def calculate_list_depth(thelist, depth=0):
    if type(thelist) is list:
        return 1 + depth + calculate_list_depth(thelist[0] if len(thelist) > 0 else None)
    else:
        return depth
