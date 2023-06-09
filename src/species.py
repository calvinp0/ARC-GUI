import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from rdkit import Chem
from rdkit.Chem import Draw
#import pandas as pd

class Species(customtkinter.CTkFrame):
    
    def __init__(self, header_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        
        # self.label = customtkinter.CTkLabel(self, text=self.header_name)
        # self.label.pack(pady=5, padx=5)
        
        self.main_frame = customtkinter.CTkScrollableFrame(self)
        self.main_frame.pack(fill='both', expand=True)
        
        # set default number of species blocks
        self.num_species_blocks = tk.StringVar()
        self.num_species_blocks.set('1')
        values = [str(i) for i in range(1, 101)]
        num_species_menu_label = customtkinter.CTkLabel(self.main_frame, text='Number of Species Blocks:', width=200)
        num_species_menu_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        num_species_menu = customtkinter.CTkComboBox(self.main_frame, width=150, values=values, variable = self.num_species_blocks, state='readonly', command=self.on_select)
        #num_species_menu = ttk.Combobox(self, width=2, textvariable=self.num_species_blocks, values=values, state='readonly')
        num_species_menu.grid(row=0, column=1)
        
        #num_species_menu.bind('<<ComboboxSelected>>', self.on_select)
        #num_species_menu.bind('<<ComboboxSelected>>', self.update_rxn_grp)
        #num_species_menu.current(0)
        self.species_blocks = []
        self.list_species_type = []
        self.list_species_entry = []
        self.species_labels_blocks = []
        self.species_checks = []
        self.type_block = []
        self.rxn_grp_blck = []
        self.img_block = []
        #self.on_select(event=int(self.num_species_blocks.get()))
        
        self.type_label = customtkinter.CTkLabel(self.main_frame, text='Type')
        self.type_label.grid(row=0, column= 6)

        self.rxn_grp_label = customtkinter.CTkLabel(self.main_frame, text='Reaction Group')
        self.rxn_grp_label.grid(row=0, column=7)
        self.rxn_dicts = dict()
        reactive_label = customtkinter.CTkLabel(self.main_frame, text="Reactive")
        reactive_label.grid(row=0, column=5, sticky='w')
        
    def on_select(self, event=None):
        # clear existing species blocks
        for block in self.species_blocks:
            block.destroy()
        self.species_blocks = []
        
        for block in self.list_species_type:
            block.destroy()
        self.list_species_type = []
        
        for block in self.list_species_entry:
            block.destroy()
        self.list_species_entry = []
        
        self.species_checks = []

        
        for block in self.species_labels_blocks:
            block.destroy()
        self.species_labels_blocks = []
        
        for block in self.type_block:
            block.destroy()
        self.type_block = []
        
        for block in self.rxn_grp_blck:
            block.destroy()
        self.rxn_grp_blck=[]
        
        for block in self.img_block:
            block.destroy()
        self.img_block=[]
        
        
        # create new species blocks
        self.num_blocks = int(self.num_species_blocks.get())
        for i in range(self.num_blocks):
            species_label = customtkinter.CTkLabel(self.main_frame, text=f'Species {i+1}:')
            species_label.grid(row=i+2, column=0, padx=5, pady=5, sticky='e')
            species_label_entry = customtkinter.CTkEntry(self.main_frame, width=200, placeholder_text="Label", placeholder_text_color="gray")
            species_label_entry.grid(row=i+2, column=1, padx=5, pady=5, sticky='w')
            
            # Values are SMILES, AdjacencyList, InChI, InChIKey, XYZ
            species_adj_smiles = customtkinter.CTkComboBox(self.main_frame, width=100, state='readonly',values=['SMILES', 'AdjacencyList', 'InChI', 'XYZ'], command=self.incr_size_)
            species_adj_smiles.grid(row=i+2, column=3, padx=5, pady=5)
            species_adj_smiles_entry = customtkinter.CTkEntry(self.main_frame, width=200, placeholder_text="SMILES/AdjList/InChI/XYZ", placeholder_text_color="gray")
            species_adj_smiles_entry.grid(row=i+2, column=4, padx=5, pady=5, sticky='w')

            reactive_var = tk.BooleanVar()
            reactive_var.set(0)
            reactive_check = customtkinter.CTkCheckBox(self.main_frame, text="", variable=reactive_var)
            reactive_check.grid(row=i+2, column=5, padx=5, pady=5,sticky='WE')
            
            type_var = tk.StringVar()
            type_var.set('')
            values = ['','Reactant', 'Product']
            type_check = customtkinter.CTkComboBox(self.main_frame, width=150, values=values, variable=type_var, state='readonly')
            type_check.grid(row=i+2, column=6)
            
            rxn_var = tk.StringVar()
            
            div = int(self.num_species_blocks.get())//2
            rxn_grps = div if div != 0 else 1
            
            #values =['Reaction 1']
            values = [f"Reaction {i}" for i in range(1,rxn_grps+1)]
            rxn_grp = customtkinter.CTkComboBox(self.main_frame, values=values,variable=rxn_var, state='readonly')
            rxn_grp.grid(row=i+2, column=7)

            self.rxn_grp_blck.append(rxn_grp)

            self.type_block.append(type_check)


            
            


            self.species_blocks.append(species_label_entry)
            self.list_species_type.append(species_adj_smiles)
            self.list_species_entry.append(species_adj_smiles_entry)
            self.species_checks.append(reactive_var)
            self.species_labels_blocks.append(species_label)
            #self.species_labels_blocks.append(species_smiles)
            self.species_labels_blocks.append(reactive_check)
            
            
            # Button to generate the image of a molecule - when clicked, the image is shown in a new window. each button is associated with a specific species block.
            show_image_button = customtkinter.CTkButton(self.main_frame, text='Show Image', command=lambda i=i: self.generate_molecule( self.list_species_type[i].get(), self.list_species_entry[i].get(), event=event))
            show_image_button.grid(row=i+2, column=8, padx=5, pady=5)
            show_image_button.configure(width = 100, height=28)
            self.img_block.append(show_image_button)
            
    def incr_size_(self, event=None):
        
        for i in range(0,len(self.species_blocks) ,3):
            #print(i)
            if self.species_blocks[i+1].get() == 'AdjacencyList':
                self.species_blocks[i+2].configure(width=200, height=200)
            elif self.species_blocks[i+1].get() == 'XYZ':
                self.species_blocks[i+2].configure(width=200, height=400)
            if self.species_blocks[i+1].get() == 'SMILES':
                self.species_blocks[i+2].configure(width = 200, height=28)
            if self.species_blocks[i+1].get() == 'InChI':
                self.species_blocks[i+2].configure(width = 200, height=28)
    def generate_molecule(self, adj_smiles_type, smiles, event=None):
        # opens a new window to display the molecule
        #print('Generating molecule')


        # Get the SMILES string in the entry box
        if adj_smiles_type is None or adj_smiles_type == '' or smiles is None:
            messagebox.showerror('Error', 'Please select a type and enter a SMILES or InChI string')
            return
        
        try:
            if adj_smiles_type == 'SMILES':
                ms = Chem.MolFromSmiles(smiles)
            elif adj_smiles_type == 'InChI':
                ms = Chem.MolFromInchi(smiles)
            image = Draw.MolToImage(ms, size=(800, 600))
            
            newWindow = customtkinter.CTkToplevel(self)
            newWindow.title('Molecule')
            newWindow.geometry('800x600')
            newWindow.resizable(False, False)
            smile_image = customtkinter.CTkImage(dark_image=image, light_image=image, size=(800, 600))
            image_label = customtkinter.CTkLabel(newWindow, image=smile_image, text='', width=800, height=600)
            image_label.pack(fill='both', expand=True)

            image_label.image = smile_image
        except Exception:
            messagebox.showerror('Error', 'Invalid SMILES string')
            return
            
    def generate_reaction_connections(self):
    # Check for empty labels
        for i in range(0, len(self.species_blocks)):
            if not self.species_blocks[i].get():
                messagebox.showerror('Error','Species label cannot be empty')
            if not self.rxn_grp_blck[i].get():
                messagebox.showerror('Error','Reaction group cannot be empty')
            if not self.type_block[i].get():
                messagebox.showerror('Error','Species type cannot be empty')

        # Check that each reaction group has at least one reactant and one product
        for i in range(0, len(self.species_blocks)):
            if self.type_block[i].get() == 'Reactant':
                for j in range(0, len(self.species_blocks)):
                    if (self.rxn_grp_blck[i].get() == self.rxn_grp_blck[j].get() 
                            and self.type_block[j].get() == 'Product'):
                        break
                else:
                    raise ValueError('Each reaction group must have at least one reactant and one product')
            elif self.type_block[i].get() == 'Product':
                for j in range(0, len(self.species_blocks)):
                    if (self.rxn_grp_blck[i].get() == self.rxn_grp_blck[j].get() 
                            and self.type_block[j].get() == 'Reactant'):
                        break
                else:
                    raise ValueError('Each reaction group must have at least one reactant and one product')

        # Construct the reaction dictionary
        self.rxn_dicts = {}
        for i in range(0, len(self.species_blocks)):
            rxn_grp = self.rxn_grp_blck[i].get()
            spec_label = self.species_blocks[i].get()
            type_rxn = self.type_block[i].get()
            self.rxn_dicts.setdefault(rxn_grp, {'Reactant': [], 'Product': [] })[type_rxn].append(spec_label)

        return self.rxn_dicts        