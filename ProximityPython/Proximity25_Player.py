# Συμμετέχοντες στην εργασία :
# Δέσποινα Δήμζα 17283 despdimz@math.auth.gr
# Κωνσταντίνος Παπάζογλου 16731 kospapazog@math.auth.gr

import random

# Δημιουργία κλάσης Cell 

class Cell:
    
    # Συνάρτηση που ορίζει τις μεταβλητές που θα δέχεται η κλάση

    def __init__(self, value, owner):
        self.value = value
        self.owner = owner

    # Συνάρτηση που επιστρέφει την τιμή του κελιού

    def getValue(self):
        return self.value

    # Συνάρτηση που ορίζει νέα τιμή για το κελί

    def setValue(self, value):
        self.value = value

    # Συνάρτηση που επιστρέφει τον παίκτη στον οποίο ανήκει το κελί

    def getOwner(self):
        return self.owner

    # Συνάρτηση που θέτει νέο ιδιοκτήτη στο κελί

    def setOwner(self, owner):
        self.owner = owner

# Δημιουργία κλάσης-παίκτη Proximity25

class Proximity25:

    # Συνάρτηση που θέτει τις μεταβλητές τις κλάσης

    def __init__(self, pid, length_X, length_Y):
        self.pid = pid
        self.length_X = length_X
        self.length_Y = length_Y

    # Συνάρτηση που ορίζει το id του παίκτη

    def setPid(self, pid):
        self.pid = pid

    # Συνάρτηση που ορίζει τις διαστάσεις του board μας

    def setBoardSize(self, length_X, length_Y):
        self.length_X = length_X
        self.length_Y = length_Y

    def getPlayerName(self):
        return "Dimza_Papazoglou"

    # Οι παρακάτω δύο μέθοδοι δημιουργήθηκαν ούτως ώστε 
    # Να δίνεται αριθμητική μεταβλητή index μέσω υπολογισμού του grid σε μορφή πίνακα
    # Ενώ η δεύτερη κρατά τη γραμμή και τη στήλη όταν της δίνεται ένα index, με την προοπτική ότι θα είναι πιο εύκολος ο τρόπος εύρεσης γειτόνων παρακάτω 
    # Θεωρήσαμε δυσκολότερο τον έλεγχο μόνο μέσω index, αφού στις οριακές τιμές θα ήταν δυσκολότερος ο έλεγχος
    # Ενώ με τον υπολογισμό του γκριντ ως πίνακα μπορούμε να αποφανθούμε καλύτερα και ευκολότερα 

    def wrap(self,row,col):
        return col + row*self.length_X


    def unwrap(self,index):
        row = index // self.length_X
        col= index - row * self.length_X
        return row, col

    # Η μέθοδος αυτή δημιουργήθηκε πρώτη με το σκεπτικό ότι είναι πιο εύκολος ο υπολογισμός 
    # των γειτόνων ενός κελιού και μετέπειτα να γίνεται ο έλεγχος για οποιοδήποτε κελί 
    # αφού εμπεριέχεται σαν τρόπος ένδειξης γειτόνων στη FindNeighbours


    def findMyNeighbours(self,index):
        neighbours = []
        row, col = self.unwrap(index)

        # Έλεγχος των γειτονικών στηλών ούτως ώστε να μην είναι εκτός Grid
        # αφού η πρώτη στήλη είναι το 0 ενώ η τελευταία το μήκος X 

        if col - 1 >= 0 :
            neighbours.append(self.wrap(row, col - 1))

        if col + 1 < self.length_X :
            neighbours.append(self.wrap(row,col + 1))

        # Έλεγχος γειτονικών γραμμών
        # Σε αυτό το σημείο βοήθησε πολύ η αντίληψη του ταμπλό ως πίνακα 
        # καθώς γίνεται έλεγχος για το αν οι γειτονικές γραμμές είναι άρτιες ή περιττές
        # όπου στη κάθε περίπτωση λόγω της μορφής του ταμπλό ο έλεγχος των στηλών αλλάζει και μετατοπίζεται 
        # και έχουμε δύο ελέγχους γιατί θέλουμε και οι γραμμές να είναι στο ταμπλό μας 

        row_above = row + 1

        row_below = row - 1

        if row_above < self.length_Y :
            neighbours.append(self.wrap(row_above,col))

            i = 1 if row_above % 2 == 0 else -1
            if col + i < self.length_X and col + i >= 0 :
                neighbours.append(self.wrap(row_above, col + i))

        if row_below >= 0 :
            neighbours.append(self.wrap(row_below,col))

            i = 1 if row_below % 2 == 0 else -1
            if col + i < self.length_X and col + i >= 0 :
                neighbours.append(self.wrap(row_below, col + i))

        return neighbours

    # Μέθοδος εύρεσης γειτόνων ανάλογα με το id και το value
    # Σε αυτή τη περίπτωση πρέπει να ελέγξουμε το κάθε κελί.
    # Για αυτό το λόγο δημιουργήσαμε μία for που αντιγράφει το ήδη υπάρχων ταμπλό και το ελέγχει 
    # ενώ διακρίνουμε τις περιπτώσεις το κελί να ανήκει σε κάποιον παίκτη ή όχι 
    # Στο τέλος, επιστρέφουμε μία λίστα με το νέο ταμπλό που περιέχει μόνο τα κελιά που ικανοποιούν τις προυποθέσεις 

    def findNeighbours(self, grid) :
        new_grid = []

        for i in range (self.length_X * self.length_Y) :
            new_cell=  Cell(grid[i].getValue(),grid[i].getOwner()) # Αντιγραφή του ταμπλό με τις τιμές στο κάθε κελί 
            if new_cell.getOwner() == 0 :           # Έλεγχος γειτονικού μη κατειλημμένου κελιού 
                neighbours = self.findMyNeighbours(i) # Εισαγωγή στη λίστα 
                for neighbour in neighbours :
                    if grid[neighbour].getOwner() > 0 : # Έλεγχος κατειλημμένου κελιού από οποιοδήποτε παίκτη
                        new_cell.setOwner(self.pid) # Μαρκαρισμένα γειτονικά από το κατειλημμένο κελιά με το δικό μας id
            new_grid.append(new_cell)
        return new_grid

    # Συνάρτηση που μας καθογεί σε σχέση με το σκορ
    # Η θετική διαφορά μας δείχνει ότι είμαστε μπροστά στη βαθμολογία
    # Το 0 ισοπαλία, ενώ η αρνητική ότι χάνουμε 
    # Η συνάρτηση αυτή είναι βοηθητική για το τρόπο που θα τοποθετήσουμε τα κελιά 

    def getScore(self, grid) :
        playerScore = 0   # Αρχικά σκορ στην αρχή του παιχνιδιού 
        opponentScore = 0
        for cell in grid : # for για τον έλεγχο κάθε κελιου και στην συνέχεια πρόσθεσει των τιμών αυτών στο σκορ του εκάστοτε παίκτη
            if cell.getOwner() == self.pid :
                playerScore = playerScore + cell.getValue()
            else :
                opponentScore = opponentScore + cell.getValue()
        return playerScore - opponentScore

    # Άλλη μία βοηθητική συνάρτηση που καθορίζει τις κινήσεις αργότερα σύμφωνα με τους κανόνες

    def applyRules(self, value, grid, index) :
        new_grid = []
        for i in range(self.length_X*self.length_Y) : # Ξανά αντιγραφή του υπάρχοντος ταμπλό για να μην γίνει κάποια ανεπιθύμητη διαστρέβλωση 
            new_cell=  Cell(grid[i].getValue(),grid[i].getOwner())
            new_grid.append(new_cell)
        new_grid[index].setValue(value)
        new_grid[index].setOwner(self.pid)
        neighbours = self.findMyNeighbours(index) 
        for i in neighbours :                       # Έλεγχος των γειτονικών κελιών για να γίνουν οι επιθυμητές αλλαγές 
            if  new_grid[i].getOwner() == self.pid :  # εδώ είναι η περίπτωση το γειτονικό κελί να είναι δικό μας και να αυξηθεί η τιμή του κατά ένα 
                new_grid[i].setValue(new_grid[i].getValue() + 1)
            elif new_grid[i].getOwner() > 0 and new_grid[i].getValue() < value : # Εδώ είναι η κατάκτηση κελιών του αντίπαλου παίκτη στη περίπτωση που η τιμή του
                new_grid[i].setOwner(self.pid)                                   # είναι μικρότερη από τη δική μας που θα τοποθετήσουμε 
        return new_grid

    # Επίσης, μία βοηθητική συνάρτηση που ελέγχει αν το ταμπλό είναι κενό σε περίπτωση που παίζουμε πρώτοι

    def isgridempty(self,grid):
        for cell in grid :
            if cell.getValue() > 0 :
                return False

        return True

    # Η συνάρτηση που οργανώνουμε τη στρατηγική μας που είναι πολύ απλή 

    def placeTile(self, value, grid) : 
        move = -1           # Ουσιαστικά θέτουμε ως κίνηση την επιλογή ενός κελιού εκτός ταμπλό για να μην χάσουμε τον έλεγχο κάποιου από αυτά
        neighbours = self.findNeighbours(grid)      # Αποθήκευση των γειτόνων 
        score = self.getScore(grid)                 # Αποθήκευση του σκορ ανάλογα με το αν έχουμε προβάδισμα ή όχι
        for i in range (self.length_X * self.length_Y) :    # Εδώ ελέγχουμε το σκορ αν πάρουμε ένα κελί ήδη μαρκαρισμένο από τη παραπάνω μέθοδο 
            if neighbours[i].getOwner() == self.pid and neighbours[i].getValue() == 0:
                new_grid = self.applyRules(value, grid, i)
                new_score = self.getScore(new_grid)         # Εισαγωγή του νέου σκορ
                if new_score > score :          # Έλεγχος, αν αυτή η κίνηση μας συμφέρει, μεταξύ των σκορ 
                    move = i
                    score = new_score
        if move == -1 and self.isgridempty(grid) :  # Εδώ έχουμε τη περίπτωση του ταμπλό να είναι κενό δηλαδή να παίζουμε πρώτοι 
            col = self.length_X // 2                # επιλέγοντας το κεντρικό κελί
            row = self.length_Y // 2
            move = self.wrap(row,col)
        if move == -1 :                         # Και εδώ αν δεν ισχύει τίποτα από τα παραπάνω, επιλέγουμε ένα τυχαίο κενό κελί
            for i in range(self.length_X*self.length_Y) :
                freecells = []
                if grid[i].getValue() == 0 :
                    freecells.append(i)
                move = random.choice(freecells)
        return move

        # Κλείνοντας έχουμε τη μέθοδο που παίρνουμε το νέο ταμπλό μετά από κάθε κίνηση 

    def applyChanges(self, value, grid) :
        move = self.placeTile(value,grid)
        new_grid = self.applyRules(value,grid,move)
        return new_grid



# Κύριο πρόγγραμμα που δείχνει την ορθή λειτουργία 

# Σε αυτή τη μέθοδο ελέγχουμε αν έχουν καταληφθεί όλα τα κελιά- λήξη παιχνιδιού

def isGridFull(grid: list[Cell]):
  for cell in grid:
    if cell.getValue() == 0:
      return False
  return True

# Εδώ έχουμε μία προσομοίωση του παιχνιδιού όπου και οι δύο παίκτες ακολουθούν τη δική μας στρατηγική
# Δε μας ενοχλεί ο παραπάνω ορισμός παικτών αφού η διαφορές που θα έχουν θα είναι μέσα στον κάθε παίκτη και το σκορ το κρατάμε ξεχωριστά

def play_game(player1: Proximity25,  player2: Proximity25, grid: list[Cell]):
    player_index = False
    players      = [player1, player2]
    while not isGridFull(grid):         # Εδώ είναι μία while που συνεχίζεται μέχρι τη λήξη
      value  = random.randint(1, 20)    # Απόδοση τυχαίων ακεραίων 

      player = players[player_index]    # Σε αυτό το σημείο καθορίζεται το ποιος παίκτης παίζει 
      grid = player.applyChanges(value, grid)       # Η κίνηση του ενεργού παίκτη 

      p_idx = 1 if not player_index else 2  # Και εδώ έχουμε την εναλλαγή μεταξύ των παικτών μόλις τελειώσει την κίνηση ο ενεργός
      player_index = not player_index

    score1,score2 = getScore(grid)     # Παίρνουμε το σκορ για κάθε παίκτη και το αποθηκεύουμε στην αντίστοιχη μεταβλητή
    print(f"Player 1 with score {score1}. Player 2 with score {score2}")

    # Εδώ έχουμε το τρόπο που παίρνουμε το σκορ, χωρίς να υπάρχει πρόβλημα που έχει ίδιο όνομα με τη παραπάνω getScore αφού είμαστε εκτός κλάσης

def getScore(grid) :
    playerScore = 0
    opponentScore = 0 
    for cell in grid : 
        if cell.getOwner() == 1 :
            playerScore = playerScore + cell.getValue()
        else :
            opponentScore = opponentScore + cell.getValue()
    return playerScore, opponentScore

# Τελικά, έχουμε τη μέθοδο που εισάγει το προφίλ των παικτών και εισάγει το grid

if __name__ == "__main__":

  index = 0
  length_X = 10
  length_Y = 10

  proximity1 = Proximity25(1, length_X, length_Y)
  proximity2 = Proximity25(2, length_X, length_Y)

  grid: list[Cell] = []
  for index in range(length_Y * length_X):
    grid.append(Cell(0,0))
  play_game(proximity1, proximity2, grid)
