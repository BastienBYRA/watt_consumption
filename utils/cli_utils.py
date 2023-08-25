from simple_term_menu import TerminalMenu
from sys import exit

class CLIUtils:
    
    def terminal_menu(self, options: list[str]):
        '''Create a terminal menu'''
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        return menu_entry_index
    
    def yes_no(self) -> int:
        '''Create a terminal menu where the user can select "Oui" or "Non"'''
        options = ["Oui", "Non"]
        return self.terminal_menu(options)
        
    def retry(self) -> bool | None:
        '''Create a terminal menu where the can retry something, if the user refuse, then exit'''
        options = ["Réesayer", "Arrêter"]
        index = self.terminal_menu(options)
        
        if index > 0: 
            exit(404)    
        return True
    
        
