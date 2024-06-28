import tkinter as tk
from tkinter import simpledialog, messagebox

class PokerApp:
    def __init__( self, root ):
        self.root = root
        self.root.title( "Poker Game Manager" )

        # Datos iniciales de los jugadores
        self.data = [
            { "Jugador": "R", "Cliente": "", "Saldo": 0.0, "Stack": 0.0, "Ciegas": 0.0, "Preflop": 0.0, "Flop": 0.0, "Turn": 0.0, "River": 0.0, "Apostado por jugador": 0.0 },
            { "Jugador": "A", "Cliente": "", "Saldo": 0.0, "Stack": 0.0, "Ciegas": 0.0, "Preflop": 0.0, "Flop": 0.0, "Turn": 0.0, "River": 0.0, "Apostado por jugador": 0.0 },
            { "Jugador": "V", "Cliente": "", "Saldo": 0.0, "Stack": 0.0, "Ciegas": 0.0, "Preflop": 0.0, "Flop": 0.0, "Turn": 0.0, "River": 0.0, "Apostado por jugador": 0.0 },
            { "Jugador": "M", "Cliente": "", "Saldo": 0.0, "Stack": 0.0, "Ciegas": 0.0, "Preflop": 0.0, "Flop": 0.0, "Turn": 0.0, "River": 0.0, "Apostado por jugador": 0.0 }
        ]

        self.crupier_saldo = 0.0
        self.rake_percentage = 20.0

        self.create_widgets()
        self.update_totals()

    def create_widgets( self ):
        cols = list( self.data[ 0 ].keys() ) + [ "Bote", "Rake", "Premio" ]

        self.entries = {}
        self.vars = {}

        for i, row in enumerate( self.data ):
            for j, col in enumerate( cols[ :-3 ] ):
                var = tk.StringVar( value = row[ col ] )
                var.trace_add( "write", lambda *args, i = i, col = col, var = var: self.update_data( i, col, var ) )
                entry = tk.Entry( self.root, textvariable = var, width = 10 )
                entry.grid( row = i + 1, column = j )
                self.entries[ ( i, col ) ] = entry
                self.vars[ ( i, col ) ] = var

        for j, col in enumerate( cols[ :-3 ] ):
            label = tk.Label( self.root, text = col )
            label.grid( row = 0, column = j )

        # Fila para totales
        self.total_vars = {}
        total_frame = tk.Frame( self.root )
        total_frame.grid( row = len( self.data ) + 2, columnspan = 4, pady = 10 )
        
        for j, col in enumerate( cols[ -3: ] ):
            label = tk.Label( total_frame, text = col )
            label.grid( row = 0, column = j * 2, padx = 5 )
            var = tk.StringVar( value = "0.0" )
            total_label = tk.Label( total_frame, textvariable = var )
            total_label.grid( row = 0, column = j * 2 + 1, padx = 5 )
            self.total_vars[ col ] = var

        # Botones de control
        control_frame = tk.Frame( self.root )
        control_frame.grid( row = len( self.data ) + 3, columnspan = 4, pady = 10 )
        tk.Button( control_frame, text = "Reset", command = self.reset_all ).grid( row = 0, column = 0, padx = 5 )
        tk.Button( control_frame, text = "Seleccionar Ganador", command = self.select_winner ).grid( row = 0, column = 1, padx = 5 )

        # Rake y saldo del crupier
        tk.Label( control_frame, text = "Rake %:" ).grid( row = 0, column = 2, padx = 5 )
        self.rake_var = tk.DoubleVar( value=self.rake_percentage )
        self.rake_var.trace_add( "write", lambda *args: self.update_totals() )
        tk.Entry( control_frame, textvariable = self.rake_var, width = 5 ).grid( row = 0, column = 3, padx = 5 )

        self.crupier_label = tk.Label( control_frame, text = f"Crupier Saldo: { self.crupier_saldo }" )
        self.crupier_label.grid( row = 0, column = 4, padx = 5 )

    def reset_all( self ):
        for row in self.data:
            for key in row:
                row[ key ] = 0.0 if key != "Jugador" else row[ key ]
        self.crupier_saldo = 0.0
        self.update_table()
        self.update_totals()
        self.crupier_label.config( text = f"Crupier Saldo: { self.crupier_saldo }" )

    def select_winner( self ):
        winner = simpledialog.askstring( "Seleccionar Ganador", "Ingrese el ganador (R, A, V, M):" )
        if winner in [ "R", "A", "V", "M" ]:
            winner_index = [ "R", "A", "V", "M" ].index( winner )
            bote_total = sum( self.data[ i ][ 'Apostado por jugador' ] for i in range( len( self.data ) ) )
            rake_total = bote_total * ( self.rake_var.get() / 100 )
            premio_total = bote_total - rake_total

            # Actualizar saldo del ganador
            self.data[ winner_index ][ 'Saldo' ] = self.data[ winner_index ][ 'Stack' ] + premio_total
            self.crupier_saldo += rake_total
            self.crupier_label.config( text = f"Crupier Saldo: { self.crupier_saldo }" )

            # Resetear las apuestas y actualizar los saldos
            for i in range( len( self.data ) ):
                if i != winner_index:
                    self.data[ i ][ 'Saldo' ] = self.data[ i ][ 'Stack' ]
                self.data[ i ][ 'Apostado por jugador' ] = 0.0
                self.data[ i ][ 'Ciegas' ] = 0.0
                self.data[ i ][ 'Preflop' ] = 0.0
                self.data[ i ][ 'Flop' ] = 0.0
                self.data[ i ][ 'Turn' ] = 0.0
                self.data[ i ][ 'River' ] = 0.0
                self.data[ i ][ 'Stack' ] = self.data[ i ][ 'Saldo' ]

            self.update_table()
            self.update_totals()
        else:
            messagebox.showerror( "Error", "Ganador no válido" )

    def update_data( self, i, col, var ):
        try:
            value = float( var.get() )
            self.data[ i ][ col ] = value

            # Actualización automática de Apostado por jugador y Stack
            if col in [ "Saldo", "Ciegas", "Preflop", "Flop", "Turn", "River" ]:
                self.data[ i ][ "Apostado por jugador" ] = sum( self.data[ i ][ key ] for key in [ "Ciegas", "Preflop", "Flop", "Turn", "River" ] )
                self.data[ i ][ "Stack" ] = self.data[ i ][ "Saldo" ] - self.data[ i ][ "Apostado por jugador" ]
                self.vars[ ( i, "Apostado por jugador" ) ].set( self.data[ i ][ "Apostado por jugador" ] )
                self.vars[ ( i, "Stack" ) ].set( self.data[ i ][ "Stack" ] )

            self.update_totals()

        except ValueError:
            self.data[ i ][ col ] = var.get()

    def update_totals( self ):
        # Actualización del Bote total
        bote_total = sum( self.data[ i ][ "Apostado por jugador" ] for i in range( len( self.data ) ) )
        self.total_vars[ "Bote" ].set( bote_total )

        # Actualización del Rake y Premio
        rake_total = bote_total * ( self.rake_var.get() / 100 )
        premio_total = bote_total - rake_total
        self.total_vars[ "Rake" ].set( rake_total )
        self.total_vars[ "Premio" ].set( premio_total )

    def update_table( self ):
        for ( i, col ), var in self.vars.items():
            var.set( self.data[ i ][ col ] )

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp( root )
    root.mainloop()
