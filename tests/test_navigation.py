import unittest
from contextlib import nullcontext
from unittest.mock import patch

from components.navigation import render_back_button


class BackButtonTests(unittest.TestCase):
    def test_compact_back_button_navigates_with_state_updates(self):
        with (
            patch("components.navigation.st.container", return_value=nullcontext()),
            patch("components.navigation.t", return_value="Back"),
            patch("components.navigation.st.button", return_value=True) as button,
            patch("components.navigation.navigate_to") as navigate_to,
        ):
            render_back_button(
                "lesson",
                compact=True,
                key="btn_back_to_collection",
                state_updates={"lesson_detail_mode": False},
            )

        button.assert_called_once_with(
            "← Back",
            key="btn_back_to_collection",
            use_container_width=False,
        )
        navigate_to.assert_called_once_with(
            "lesson",
            lesson_detail_mode=False,
        )

    def test_compact_back_button_does_not_navigate_when_not_clicked(self):
        with (
            patch("components.navigation.st.container", return_value=nullcontext()),
            patch("components.navigation.t", return_value="Kembali"),
            patch("components.navigation.st.button", return_value=False),
            patch("components.navigation.navigate_to") as navigate_to,
        ):
            render_back_button("dashboard", compact=True)

        navigate_to.assert_not_called()


if __name__ == "__main__":
    unittest.main()
