from data_utils import load_data
from layout_components import (
    display_beetle_comparison,
    display_beetle_details,
    sidebar_search_filter,
)
from style_utils import apply_styles, set_page_config


def main():
    """
    Main function to run the Streamlit app.
    """
    # Page configuration
    set_page_config()
    apply_styles()

    # Load data
    beetles_data = load_data()

    # Sidebar search and filter
    selected_beetle, all_names, name_to_index, selected_index = sidebar_search_filter(
        beetles_data
    )

    # Display beetle details
    display_beetle_details(selected_beetle, beetles_data)

    # Display beetle comparison
    display_beetle_comparison(beetles_data, all_names, name_to_index, selected_index)


if __name__ == "__main__":
    main()
