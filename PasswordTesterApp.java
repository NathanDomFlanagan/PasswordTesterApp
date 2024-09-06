import javax.swing.*;
import java.awt.*;

public class PasswordTesterApp extends JFrame
{
    public PasswordTesterApp() 
    {
        setTitle("Password Tester");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(650, 550);
        setLocationRelativeTo(null);

        // Create components
        JButton buttonShowTips = new JButton("Show Tips");
        //TODO: Look into other options other than HTML for the Tips
        buttonShowTips.addActionListener(e -> JOptionPane.showMessageDialog(null, "<html><ul>" +
                    "<li>At least 8 characters long</li>" +
                    "<li>Not a repeated password</li>" +
                    "<li>Not a generic password</li>" +
                    "<li>Contains at least one uppercase letter</li>" +
                    "<li>Contains at least one lowercase letter</li>" +
                    "<li>Contains at least one digit</li>" +
                    "<li>Contains at least one special character (e.g., !@#$%^&*())</li>" +
                    "</ul></html>", "Password Tips", JOptionPane.INFORMATION_MESSAGE));

        JLabel labelPassword = new JLabel("Enter your password:");
        labelPassword.setFont(new Font("Arial", Font.BOLD, 14));
        //labelPassword.setForeground(Color.BLACK);

        JTextField textFieldPassword = new JTextField(20);
        JButton buttonTestPassword = new JButton("Test Password");
        buttonTestPassword.setFont(new Font("Arial", Font.PLAIN, 14));

        JLabel labelFeedback = new JLabel();
        labelFeedback.setFont(new Font("Arial", Font.ITALIC, 12));
        labelFeedback.setForeground(Color.RED);
        
        // Add action listener to the button using lambda expression
        buttonTestPassword.addActionListener(e -> {
            String password = textFieldPassword.getText();
            // Test the password
            boolean isSecure = PasswordChecker.isPasswordSecure(password, labelFeedback);; 
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
}