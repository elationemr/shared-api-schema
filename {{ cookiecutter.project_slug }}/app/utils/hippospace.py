from el8.ext.services.context import get_elation_context


def get_current_hippospace() -> str:
    """
    Get hippospace from the current request context.

    This function can be used as FastAPI dependency. For example:
    ```    def my_route(hippospace: str = Depends(get_current_hippospace)):
      ...
    ```

    Returns:
        str: The hippospace value.
    """
    return get_elation_context().hippospace
