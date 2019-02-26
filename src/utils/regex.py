def build_regexpr_from_list(items):
    """
    Builds a regex that matches exactly any item in items
    """
    or_expr = "|".join([x + '{1}' for x in items])
    expr = r'(?:%s)' % or_expr
    return expr