import cv2
import numpy as np


class ImageGridDivider:
    """Divides an image into a grid and resizes each section to a target size."""

    def __init__(
            self,
            rows: int,
            cols: int,
            target_size: tuple[int, int],
            group_by: str = 'y'
    ):
        """Initializes the ImageGridDivider with grid specifications.

        Args:
            rows (int): Number of rows to divide the image into.
            cols (int): Number of columns to divide the image into.
            target_size (tuple[int, int]): Desired size of each section after resizing.
            group_by (str, optional): Axis to group by, either 'y' for rows or 'x' for columns. Defaults to 'y'.
        """
        self.rows = rows
        self.cols = cols
        self.target_size = target_size
        self.group_by = group_by

    def divide(self, image: np.ndarray) -> np.ndarray:
        """Divides an image into a grid and resizes each section to the target size.

        Args:
            image (np.ndarray): The image to divide.

        Returns:
            np.ndarray: A 4D numpy array containing the divided and resized image sections, grouped by the specified axis.

        Raises:
            ValueError: If `group_by` is neither 'y' nor 'x'.
        """
        # Calculate expected dimensions.
        expected_height = self.target_size[0] * self.rows
        expected_width = self.target_size[1] * self.cols

        # Resize image to fit exact grid of sections.
        resized_image = cv2.resize(
            image, (expected_width, expected_height), interpolation=cv2.INTER_LINEAR
        )

        # Calculate individual section positions.
        y_positions = [i * self.target_size[0] for i in range(self.rows)]
        x_positions = [i * self.target_size[1] for i in range(self.cols)]

        # Extract sections.
        if self.group_by == 'y':
            # Group by rows.
            sections = [
                [
                    resized_image[
                        y:y + self.target_size[0],
                        x:x + self.target_size[1]
                    ]
                    for x in x_positions
                ]
                for y in y_positions
            ]
        elif self.group_by == 'x':
            # Group by columns.
            sections = [
                [
                    resized_image[
                        y:y + self.target_size[0],
                        x:x + self.target_size[1]
                    ]
                    for y in y_positions
                ]
                for x in x_positions
            ]
        else:
            raise ValueError("group_by must be either 'y' or 'x'")

        return np.array(sections)
