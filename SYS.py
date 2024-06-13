import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import simpledialog

class InventoryGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("재고 관리 시스템")

        self.inventory = {}

        self.product_label = tk.Label(master, text="제품명:")
        self.product_label.grid(row=0, column=0, padx=10, pady=10)
        self.product_entry = tk.Entry(master)
        self.product_entry.grid(row=0, column=1, padx=10, pady=10)

        self.quantity_label = tk.Label(master, text="수량:")
        self.quantity_label.grid(row=1, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(master)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(master, text="제품 추가", command=self.add_product, width=40)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.sell_button = tk.Button(master, text="제품 판매", command=self.sell_product, width=40)
        self.sell_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.save_button = tk.Button(master, text="저장", command=self.save_inventory, width=40)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.load_button = tk.Button(master, text="불러오기", command=self.load_inventory, width=40)
        self.load_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.inventory_textbox = scrolledtext.ScrolledText(master, width=40, height=10)
        self.inventory_textbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.inventory_textbox.config(state=tk.DISABLED)  # 텍스트 상자 비활성화

        self.load_inventory()  # 초기화면에서 재고를 파일에서 불러옴

        # 텍스트 상자에서 마우스 오른쪽 버튼 클릭 이벤트 바인딩
        self.inventory_textbox.bind("<Button-3>", self.show_context_menu)

        # 우클릭 메뉴 생성
        self.context_menu = tk.Menu(master, tearoff=0)
        self.context_menu.add_command(label="수량 수정", command=self.edit_selected_item)

        # 윈도우 종료 이벤트에 자동 저장 기능 바인딩
        self.master.protocol("WM_DELETE_WINDOW", self.save_and_quit)

    def add_product(self):
        product = self.product_entry.get()
        quantity = int(self.quantity_entry.get())
        if product in self.inventory:
            self.inventory[product] += quantity
        else:
            self.inventory[product] = quantity
        messagebox.showinfo("성공", f"{product}를 재고에 추가했습니다.")
        self.update_inventory_textbox()

    def sell_product(self):
        product = self.product_entry.get()
        quantity = int(self.quantity_entry.get())
        if product in self.inventory:
            if self.inventory[product] >= quantity:
                self.inventory[product] -= quantity
                messagebox.showinfo("성공", f"{quantity}개의 {product}를 판매했습니다.")
            else:
                messagebox.showerror("오류", "재고가 부족합니다.")
        else:
            messagebox.showerror("오류", "해당 제품이 재고에 없습니다.")
        self.update_inventory_textbox()

    def save_inventory(self):
        with open("inventory.txt", "w") as f:
            for product, quantity in self.inventory.items():
                f.write(f"{product}:{quantity}\n")
        messagebox.showinfo("저장 완료", "재고를 파일에 저장했습니다.")

    def load_inventory(self):
        self.inventory.clear()
        try:
            with open("inventory.txt", "r") as f:
                for line in f:
                    product, quantity = line.strip().split(":")
                    self.inventory[product] = int(quantity)
            messagebox.showinfo("불러오기 완료", "파일에서 재고를 불러왔습니다.")
            self.update_inventory_textbox()
        except FileNotFoundError:
            messagebox.showerror("오류", "재고 파일을 찾을 수 없습니다.")

    def update_inventory_textbox(self):
        self.inventory_textbox.config(state=tk.NORMAL)  # 텍스트 상자 활성화
        self.inventory_textbox.delete('1.0', tk.END)
        for product, quantity in self.inventory.items():
            self.inventory_textbox.insert(tk.END, f"{product}: {quantity}\n")
        self.inventory_textbox.config(state=tk.DISABLED)  # 텍스트 상자 비활성화

    def show_context_menu(self, event):
    # 오른쪽 버튼을 클릭한 위치의 텍스트를 선택
        index = self.inventory_textbox.index("@{},{}".format(event.x, event.y))
        self.inventory_textbox.tag_add(tk.SEL, index)
        self.context_menu.post(event.x_root, event.y_root)

    def edit_selected_item(self):
        selected_text = self.inventory_textbox.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            selected_product, selected_quantity = selected_text.strip().split(":")
            new_quantity = simpledialog.askinteger("수량 수정", f"{selected_product}의 새로운 수량을 입력하세요:")
            if new_quantity is not None:
                self.inventory[selected_product] = new_quantity
                messagebox.showinfo("성공", f"{selected_product}의 수량을 수정했습니다.")
                self.update_inventory_textbox()
        else:
            messagebox.showwarning("경고", "텍스트를 먼저 선택하세요.")

    def save_and_quit(self):
        self.save_inventory()  # 종료 전에 자동으로 저장
        self.master.quit()  # 프로그램 종료

def main():
    root = tk.Tk()
    inventory_gui = InventoryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()