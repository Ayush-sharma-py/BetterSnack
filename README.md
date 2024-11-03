# Better Snack - README

## Overview

**Better Snack** is a Streamlit application that helps users find and evaluate snack products based on their names and brands. It utilizes fuzzy matching algorithms to enhance product name recognition and allows filtering by brand for more precise results.

## Technologies Used

- **Streamlit**: A framework for building interactive web applications in Python, enabling rapid development of data-driven apps.
- **RapidFuzz**: A library for fuzzy string matching that helps compare product names and brands efficiently.
- **Pandas**: A powerful data manipulation and analysis library for Python, used for handling the product dataset.
- **NumPy**: A library for numerical computing in Python, providing support for large, multi-dimensional arrays and matrices.
- **CSV**: The application reads data from a CSV file (`filtered.csv`), which contains product details.

## Features

- **Product Name Lookup**: Users can enter a snack name to find matches in the dataset, utilizing fuzzy string matching for improved accuracy.
- **Brand Filtering**: Optional brand name input to further narrow down search results.
- **Dynamic Visualization**: The application displays relevant product details such as Nova Group, Nutri Score, and Nutri Grade with visually distinct indicators.
- **Caching**: Efficient data loading with caching mechanisms to improve app performance.

## Requirements

To run the application, ensure you have the following Python packages installed:

```bash
pip install streamlit rapidfuzz pandas numpy
```

## Usage

1. **Load the Data**: The application reads the dataset from `Data/Files/filtered.csv`. Ensure this file exists and is properly formatted.
2. **Run the App**: Use the following command to start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. **Interact with the App**:
   - Enter a snack name in the provided input field.
   - Optionally, enter a brand name to filter results.
   - The app will display matching products along with relevant nutritional information.

## Code Structure

- **Functions**:
  - `load_data()`: Loads and caches the product data from a CSV file.
  - `lookupProductName()`: Finds products matching the input name using fuzzy matching.
  - `filterBrand()`: Filters the resulting products by the specified brand name.
  - `lookupBestMatch()`: Identifies the best match from the filtered results.
  - `printRow()`: Displays the product information in a formatted way on the Streamlit app.

## Contribution

Contributions to improve the application are welcome! Feel free to fork the repository and submit a pull request with enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For any questions or issues, please feel free to reach out! Enjoy discovering your snacks!