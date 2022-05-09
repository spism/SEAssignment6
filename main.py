from pizza import Pizza
from order import Order
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def main():
    p = Pizza(0,"Margh",True,19.99,["aaaa","fff"])
    o = Order(1,143344,"waiting","10.7. 2020","i am cool",True,"Apple pay","phs3",[p])
    print(o.to_json())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
