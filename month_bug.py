#Printing out a interger correlated with a month
def main():
    #First receiving input from user
    n = eval(input("Please provide a number 1 to 12 for the month we are in: "))
    pos = n - 1
    #Have the input from user display the correlating month with number
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    print("The month is: ", months[pos])


main()
