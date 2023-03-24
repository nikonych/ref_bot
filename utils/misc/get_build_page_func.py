import utils.pagination


def get_build_page_func(build_page_path: str):
    build_page_module, build_page_func = build_page_path.split('.')

    module = getattr(utils.pagination, build_page_module)
    func = getattr(module, build_page_func)

    return func
