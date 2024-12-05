import javax.swing.SwingUtilities;

public class Main 
{
    public static void main(String[] args) 
    {
        // SwingUtilities.invokeLater(new Runnable() 
        // {
        //     @Override
        //     public void run() 
        //     {
        //         PasswordTesterApp app = new PasswordTesterApp();
        //         app.setVisible(true);
        //     }
        // });

        //Used recommended lambda expression
        SwingUtilities.invokeLater(() -> {
            //Maybe look into making a simple password generator
            //Make a Class that prompts either password tester or the password generator GUI
            PasswordTesterApp app = new PasswordTesterApp();
            app.setVisible(true);
        });
    }
}