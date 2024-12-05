import javax.swing.JLabel;

public class PasswordChecker 
{
    public static boolean isPasswordSecure(String password, JLabel labelFeedback) 
    {
        // Implement password testing parameters here
        // For example, check length, complexity, etc.
        //return password.length() >= 8 && password.matches(".*[A-Z].*") && password.matches(".*[a-z].*") && password.matches(".*\\d.*") && password.matches(".*[!@#$%^&*()].*");
        
        // If password is less than 8 then prompted to make a longer one
        if (password.length() < 8) 
        {
            labelFeedback.setText("Password is too short. It should be at least 8 characters long.");
            return false;
        }
        // If password doesn't contain a capital letter then prompted to add one
        if (!password.matches(".*[A-Z].*")) 
        {
            labelFeedback.setText("Password should contain at least one uppercase letter.");
            return false;
        }
        // If password doesn't contain a lowercase letter then prompted to add one
        if (!password.matches(".*[a-z].*")) 
        {
            labelFeedback.setText("Password should contain at least one lowercase letter.");
            return false;
        }
        // If passowrd doesn't contain at least one digit then prompted to add one
        if (!password.matches(".*\\d.*")) 
        {
            labelFeedback.setText("Password should contain at least one digit.");
            return false;
        }
        // If password doesn't contain one special character then prompted to add one
        if (!password.matches(".*[!@#$%^&*()].*")) 
        {
            labelFeedback.setText("Password should contain at least one special character (e.g., !@#$%^&*()).");
            return false;
        }
        return true;
    }    
}