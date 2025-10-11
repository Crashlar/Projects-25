import numpy as np

class ScratchLinearRegression:
    """
    A custom implementation of linear regression using ordinary least squares method.
    This class provides fundamental linear regression capabilities for educational
    and analytical purposes.
    """
    
    def __init__(self):
        """
        Initialize the linear regression model.
        
        Attributes:
        m (float): Slope coefficient of the regression line
        b (float): Intercept term of the regression line
        """
        self.m = None
        self.b = None
        
    def fit(self, X, y):
        """
        Train the linear regression model on the provided dataset.
        
        Parameters:
        X (array-like): Independent variable values (feature)
        y (array-like): Dependent variable values (target)
        
        Raises:
        ValueError: If the denominator in slope calculation is zero
        """
        # Convert inputs to numpy arrays with explicit float typing
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)
        
        # Calculate central tendencies
        X_mean = np.mean(X)
        y_mean = np.mean(y)
        
        # Compute regression coefficients using OLS method
        numerator = np.sum((X - X_mean) * (y - y_mean))
        denominator = np.sum((X - X_mean) ** 2)
        
        # Validate calculation conditions
        if denominator == 0:
            raise ValueError("Cannot compute regression coefficients: "
                           "Variance in independent variable is zero.")
            
        self.m = numerator / denominator
        self.b = y_mean - self.m * X_mean
        
    def predict(self, X):
        """
        Generate predictions using the trained regression model.
        
        Parameters:
        X (array-like or scalar): Input values for prediction
        
        Returns:
        array or scalar: Predicted values based on the regression model
        
        Raises:
        ValueError: If the model has not been trained
        """
        if self.m is None or self.b is None:
            raise ValueError("Model must be trained before generating predictions.")
        
        # Ensure input is properly formatted
        X = np.array(X, dtype=float)
            
        return self.m * X + self.b
    
    def get_parameters(self):
        """
        Retrieve the trained model parameters.
        
        Returns:
        dict: Dictionary containing slope and intercept parameters
        """
        return {
            'slope_coefficient': self.m, 
            'intercept_term': self.b
        }
    
    def calculate_r_squared(self, X, y):
        """
        Compute the coefficient of determination (R-squared) for model evaluation.
        
        Parameters:
        X (array-like): Independent variable values
        y (array-like): Actual target values
        
        Returns:
        float: R-squared value indicating model explanatory power
        """
        # Convert inputs to appropriate format
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float)
        
        # Generate predictions
        y_pred = self.predict(X)
        y_mean = np.mean(y)
        
        # Calculate sum of squares
        ss_residual = np.sum((y - y_pred) ** 2)
        ss_total = np.sum((y - y_mean) ** 2)
        
        # Handle edge case
        if ss_total == 0:
            return 0.0
            
        return 1 - (ss_residual / ss_total)