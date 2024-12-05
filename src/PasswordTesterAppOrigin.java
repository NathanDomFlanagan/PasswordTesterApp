import java.awt.*;
import java.awt.event.ActionEvent;
import javax.swing.*;

public class PasswordTesterAppOrigin extends JFrame 
{

    private JTextField textFieldPassword;
    private JLabel labelFeedback;

    public PasswordTesterAppOrigin() 
    {
        setTitle("Password Tester");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(650, 550);
        setLocationRelativeTo(null);

        // Create components
        JButton buttonShowTips = new JButton("Show Tips");
        buttonShowTips.addActionListener((ActionEvent e) -> {
            JOptionPane.showMessageDialog(null, "<html><ul>" +
                    "<li>At least 8 characters long</li>" +
                    "<li>Not a repeated password</li>" +
                    "<li>Not a generic password</li>" +
                    "<li>Contains at least one uppercase letter</li>" +
                    "<li>Contains at least one lowercase letter</li>" +
                    "<li>Contains at least one digit</li>" +
                    "<li>Contains at least one special character (e.g., !@#$%^&*())</li>" +
                    "</ul></html>", "Password Tips", JOptionPane.INFORMATION_MESSAGE);
        });

        JLabel labelPassword = new JLabel("Enter your password:");
        textFieldPassword = new JTextField(20);
        JButton buttonTestPassword = new JButton("Test Password");
        labelFeedback = new JLabel();

        // Add action listener to the button
        buttonTestPassword.addActionListener((ActionEvent e) -> {
            String password = textFieldPassword.getText();
            // Test the password
            boolean isSecure = isPasswordSecure(password); 
            // Provide feedback to the user
            if (isSecure)
            {
                labelFeedback.setText("Password is secure."); 
            }
        });

        // Create layout
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(5, 1));
        panel.add(buttonShowTips);
        panel.add(new JLabel(" "));
        panel.add(labelPassword);
        panel.add(textFieldPassword);
        panel.add(buttonTestPassword);

        JPanel feedbackPanel = new JPanel();
        feedbackPanel.add(labelFeedback);

        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(panel, BorderLayout.NORTH);
        getContentPane().add(feedbackPanel, BorderLayout.CENTER);
    }

    private boolean isPasswordSecure(String password) 
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

    public static void main(String[] args) 
    {
        SwingUtilities.invokeLater(() -> {
            PasswordTesterAppOrigin app = new PasswordTesterAppOrigin();
            app.setVisible(true);
        });
    }
}
