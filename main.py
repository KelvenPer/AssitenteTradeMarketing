import tkinter as tk
from tkinter import Canvas, Scrollbar, VERTICAL, HORIZONTAL, RIGHT, LEFT, Y, X, BOTH, NW, BOTTOM
import json

# Carregar o JSON a partir de um arquivo
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

class FlowchartApp:
    def __init__(self, root, data):
        self.root = root
        self.root.title("Assistente de Trade Marketing - Fluxograma")
        self.canvas = Canvas(root, bg="white", width=1200, height=800, scrollregion=(0,0,3000,3000))
        
        # Adicionar barras de rolagem
        self.v_scroll = Scrollbar(root, orient=VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=RIGHT, fill=Y)
        self.h_scroll = Scrollbar(root, orient=HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.pack(side=BOTTOM, fill=X)
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.data = data
        self.box_width = 300
        self.box_height = 50
        self.x_gap = 50
        self.y_gap = 30
        self.current_x = self.x_gap
        self.current_y = self.y_gap
        self.level_offsets = {}  # Para manter a posição de cada nível

        # Iniciar o desenho do fluxograma
        self.draw_flowchart()

    def draw_flowchart(self):
        # Desenhar o título principal
        self.draw_box(self.data["title"], self.current_x, self.current_y, "lightblue")
        self.current_y += self.box_height + self.y_gap

        # Iterar sobre as seções
        for section in self.data["sections"]:
            self.process_section(section, indent=0)

    def process_section(self, section, indent):
        x = self.current_x + indent * (self.box_width + self.x_gap)
        y = self.current_y

        # Desenhar a caixa da seção
        self.draw_box(section["title"], x, y, "lightgreen")
        
        # Conectar com a seção anterior se não for o primeiro
        if indent > 0:
            parent_x = x - (self.box_width + self.x_gap)
            parent_y = y - (self.box_height + self.y_gap)
            self.draw_line(parent_x + self.box_width, parent_y + self.box_height, x, y)
        
        self.current_y = y + self.box_height + self.y_gap

        # Desenhar os itens da seção
        if "items" in section:
            for item in section["items"]:
                self.draw_box(item, x + 20, self.current_y, "lightyellow")
                self.draw_line(x + self.box_width, self.current_y - self.y_gap, x + 20, self.current_y)
                self.current_y += self.box_height + self.y_gap

        # Desenhar as subseções recursivamente
        if "subsections" in section:
            for subsection in section["subsections"]:
                self.process_section(subsection, indent + 1)

    def draw_box(self, text, x, y, color):
        # Desenhar retângulo
        self.canvas.create_rectangle(x, y, x + self.box_width, y + self.box_height, fill=color, outline="black")
        # Adicionar texto
        self.canvas.create_text(x + self.box_width/2, y + self.box_height/2, text=text, font=("Arial", 10), width=self.box_width-10)

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

def main():
    # Carregar o JSON
    json_data = load_json('trade_marketing.json')

    root = tk.Tk()
    app = FlowchartApp(root, json_data)
    root.mainloop()

if __name__ == "__main__":
    main()
