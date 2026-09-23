import java.util.Scanner;

public class seats 
{
    public static void main(String[] args) 
    {
        if(args.length < 3) 
        {
            System.out.println("ERROR: Missing parameters");
            System.exit(1);
        }

        int row = Integer.parseInt(args[0]);
        int col = Integer.parseInt(args[1]);
        int isBooked = Integer.parseInt(args[2]);

        if(isBooked == 1) 
        {
            System.out.println("REJECTED: Seat (" + row + "," + col + ") is already occupied.");
            System.exit(1); 
        } 
        
        else 
        {
            System.out.println("APPROVED: Seat (" + row + "," + col + ") is available.");
            System.exit(0); 
        }
    }
}