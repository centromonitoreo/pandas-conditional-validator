from .base import HandlerError


class DeleteRowError(HandlerError):

    """Error handler for delete row operations."""

    def handle_error(self, df, conditions) -> None:
        """Handle the delete row error."""
        
        df = df[conditions]
        return df