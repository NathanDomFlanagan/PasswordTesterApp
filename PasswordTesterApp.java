import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class PasswordTesterApp extends JFrame {

    private JTextField textFieldPassword;
    private JLabel labelFeedback;

    public PasswordTesterApp() {
        setTitle("Password Tester");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(600, 500);
        setLocationRelativeTo(null);

        // Create components
        JLabel labelPassword = new JLabel("Enter your password:");
        textFieldPassword = new JTextField(20);
        JButton buttonTestPassword = new JButton("Test Password");
        labelFeedback = new JLabel();

        // Add action listener to the button
        buttonTestPassword.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String password = textFieldPassword.getText();
                // Test the password
                boolean isSecure = isPasswordSecure(password);
                // Provide feedback to the user
                if (isSecure) {
                    labelFeedback.setText("Password is secure.");
                } else {
                    labelFeedback.setText("Password is not secure. Please choose a stronger password.");
                }
            }
        });

        // Create layout
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(3, 1));
        panel.add(labelPassword);
        panel.add(textFieldPassword);
        panel.add(buttonTestPassword);

        JPanel feedbackPanel = new JPanel();
        feedbackPanel.add(labelFeedback);

        getContentPane().setLayout(new BorderLayout());
        getContentPane().add(panel, BorderLayout.NORTH);
        getContentPane().add(feedbackPanel, BorderLayout.CENTER);
    }

    private boolean isPasswordSecure(String password) {
        // Implement password testing logic here
        // For example, check length, complexity, etc.
        return password.length() >= 8 && password.matches(".*[A-Z].*") && password.matches(".*[a-z].*") && password.matches(".*\\d.*") && password.matches(".*[!@#$%^&*()].*");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                PasswordTesterApp app = new PasswordTesterApp();
                app.setVisible(true);
            }
        });
    }
}
