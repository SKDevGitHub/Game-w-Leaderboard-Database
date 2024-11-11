import pygame
import random
import math

pygame.init()

width, height = 800, 600
tileSize = 60
window = pygame.display.set_mode((width, height))

pygame.display.set_caption("Dungeon Crawler")

floorImg = pygame.image.load('assets/floor.png')
wallImg = pygame.image.load('assets/wall.png')
demonImg = pygame.image.load('assets/demon.png')
ogreImg = pygame.image.load('assets/ogre.png')
actManImg = pygame.image.load('assets/act-man.png')
corpseImg = pygame.image.load('assets/corpse.png')

floorImg = pygame.transform.scale(floorImg, (tileSize, tileSize))
wallImg = pygame.transform.scale(wallImg, (tileSize, tileSize))
demonImg = pygame.transform.scale(demonImg, (tileSize, tileSize))
ogreImg = pygame.transform.scale(ogreImg, (tileSize, tileSize))
actManImg = pygame.transform.scale(actManImg, (tileSize, tileSize))
corpseImg = pygame.transform.scale(corpseImg, (tileSize, tileSize))

moveMap = {
    pygame.K_w: (-1, 0),        # Up
    pygame.K_d: (0, 1),         # Right
    pygame.K_s: (1, 0),         # Down
    pygame.K_a: (0, -1),        # Left
    pygame.K_e: (-1, 1),        # Diagonal Up-Right
    pygame.K_q: (-1, -1),       # Diagonal Up-Left
    pygame.K_x: (1, 1),         # Diagonal Down-Right
    pygame.K_z: (1, -1)         # Diagonal Down-Left
}

def boardLoader(filename):
    board = []
    with open(filename, 'r') as file:
        for line in file:
            row = list(line.strip())
            board.append(row)
    return board

def drawBoard(board):
    for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == "#":
                    window.blit(wallImg, (col * tileSize, row * tileSize))
                elif board[row][col] == " ":
                    window.blit(floorImg, (col * tileSize, row * tileSize))
                elif board[row][col] == "A":
                    window.blit(actManImg, (col * tileSize, row * tileSize))
                elif board[row][col] == "G":
                    window.blit(ogreImg, (col * tileSize, row * tileSize))
                elif board[row][col] == "D":
                    window.blit(demonImg, (col * tileSize, row * tileSize))
                elif board[row][col] == "@":
                    window.blit(corpseImg, (col * tileSize, row * tileSize))
                    
def movePlayer(board, direction, playerPos):
    newX = playerPos[0] + direction[0]
    newY = playerPos[1] + direction[1]
    if 0 <= newX < len(board) and 0 <= newY < len(board[0]) and board[newX][newY] != "#":
        board[playerPos[0]][playerPos[1]] = " "
        playerPos = [newX, newY]
        board[playerPos[0]][playerPos[1]] = "A"
    return playerPos
    
def handlePlayerMovement(board, playerPos):
    keys = pygame.key.get_pressed()

    # Check for diagonal movement
    if keys[pygame.K_e]:
        direction = (-1, 1)  # Up-Right
    elif keys[pygame.K_q]:
        direction = (-1, -1)  # Up-Left
    elif keys[pygame.K_x]:
        direction = (1, 1)  # Down-Right
    elif keys[pygame.K_z]:
        direction = (1, -1)  # Down-Left
    # Check for single direction movement
    elif keys[pygame.K_w]:
        direction = (-1, 0)  # Up
    elif keys[pygame.K_s]:
        direction = (1, 0)  # Down
    elif keys[pygame.K_a]:
        direction = (0, -1)  # Left
    elif keys[pygame.K_d]:
        direction = (0, 1)  # Right
    else:
        direction = None
    
    if direction:
        playerPos = movePlayer(board, direction, playerPos)

    return playerPos    
    
def euclidDistance(xy1, xy2):
    return math.dist(xy2, xy1)

def enemyCounter(state):
    # always in order ogres, demons
    ocount = sum(row.count("G") for row in state)
    dcount = sum(row.count("D") for row in state)
    return ocount, dcount


def getAdjacentCells(xy, c, r):
    adjacent = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and 0 <= xy[0] + dx < c and 0 <= xy[1] + dy < r:
                adjacent.append([xy[0] + dx, xy[1] + dy])
    return adjacent

def monsterRemove(gameState, shrek, muzan):
    for x in shrek:
        gameState[x[0]][x[1]] = " "
    for y in muzan:
        gameState[y[0]][y[1]] = " "
    return

#moves the ogres
def ogreMash(gameState, oCoord, amCoord, gSX, gSY):
    possibleo = getAdjacentCells(oCoord, gSX, gSY)
    distanceMino = float('inf')
    besto = None
    clockwise = [[-1, 0], [-1, 1], [0, 1], [1, 1],
                 [1, 0], [1, -1], [0, -1], [-1, -1]]
    bestcounto = []
    for moveo in possibleo:
        dg = oCoord
        if gameState[moveo[0]][moveo[1]] != "#":
            disto = euclidDistance(moveo, amCoord)
            if distanceMino == None:
                distanceMino = disto
            elif disto < distanceMino:
                distanceMino = disto
                besto = moveo
                bestcounto = [x-y for x, y in zip(moveo, dg)]
            elif disto == distanceMino:
                checko = [x-y for x, y in zip(moveo, dg)]
                if clockwise.index(checko) < clockwise.index(bestcounto):
                    besto = moveo
                    bestcounto = checko
    return besto

def demonMash(gameState, dCoord, amCoord, gsX, gsY):
    possible = getAdjacentCells(dCoord, gsX, gsY)
    distanceMin = float('inf')
    best = None
    countClockwise = [[-1, 0], [-1, -1], [0, -1],
                      [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]
    bestcount = []
    for move in possible:
        og = dCoord
        if gameState[move[0]][move[1]] != "#":
            dist = euclidDistance(move, amCoord)
            if distanceMin == None:
                distanceMin = dist
            elif dist < distanceMin:
                distanceMin = dist
                best = move
                bestcount = [x-y for x, y in zip(move, og)]
            elif dist == distanceMin:
                check = [x-y for x, y in zip(move, og)]
                if countClockwise.index(check) < countClockwise.index(bestcount):
                    best = move
                    bestcount = check
    return best

#checks all the collision possibilities between the enemy types
def monsterCollideCheck(shrek, muzan, gameState, coord, deadAsHell, num):
    for x in shrek:
        if shrek.count(x) > 1:
            gameState[x[0]][x[1]] = "@"
            deadAsHell.append(x)
            for p in shrek:
                if p == x:
                    shrek.remove(x)
        if x in muzan:
            gameState[x[0]][x[1]] = "@"
            if x in shrek:
                shrek.remove(x)
                muzan.remove(x)
            if x not in deadAsHell:
                deadAsHell.append(x)
        if x in deadAsHell:
            if x in shrek:
                shrek.remove(x)
                gameState[x[0]][x[1]] = "@"
    for y in muzan:
        if muzan.count(y) > 1:
            gameState[y[0]][y[1]] = "@"
            deadAsHell.append(y)
            for h in muzan:
                if h == y:
                    muzan.remove(y)
        if y in deadAsHell:
            if y in muzan:
                muzan.remove(y)
                gameState[y[0]][y[1]] = "@"
    if ((coord in shrek) or (coord in muzan) or (coord in deadAsHell)) and coord != "X":
        gameState[coord[0]][coord[1]] == "X"
        num = 0
    return num

def findEnemyPos(state, r, c, ogre, demon, corpse):
    for x in range(r):
        for y in range(c):
            if state[x][y] == "G":
                ogre.append([x, y])
            if state[x][y] == "D":
                demon.append([x, y])
            if state[x][y] == "@":
                corpse.append([x, y])
    return

def monsterAdd(gameState, shrek, muzan):
    for x in shrek:
        if gameState[x[0]][x[1]] != "X":
            if gameState[x[0]][x[1]] == "A":
                gameState[x[0]][x[1]] = "X"
            else:
                gameState[x[0]][x[1]] = "G"
    for y in muzan:
        if gameState[y[0]][y[1]] != "X":
            if gameState[y[0]][y[1]] == "A":
                gameState[y[0]][y[1]] = "X"
            else:
                gameState[y[0]][y[1]] = "D"
    return

def displayGameOver(score, result):
    print("GAME OVER")
    font = pygame.font.SysFont(None, 55)
    gameOverText = font.render(f"Game Over: {result}", True, (255, 0, 0))
    scoreText = font.render(f"Final Score: {score}", True, (255, 255, 255))
    
    window.fill((0, 0, 0))  # Clear the screen
    window.blit(gameOverText, (width // 2 - 150, height // 2 - 50))
    window.blit(scoreText, (width // 2 - 150, height // 2 + 20))
    pygame.display.update()
    
    pygame.time.delay(3000)

def main():
    board = boardLoader('board1.txt')
    rows = len(board)
    columns = len(board[0])

    running = True
    clock = pygame.time.Clock()
    
    playerTurn = True
    playerMoved = False
    gameOver = False
    playerWon = False

    ogreCount, demonCount = enemyCounter(board)

    while running:
        window.fill((0,0,0))
        
        ogres = []
        demons = []
        corpses = []
        moveList = []
        turnCount = 0
        score = 50
        
        findEnemyPos(board, rows, columns, ogres, demons, corpses)
        
        drawBoard(board)
        pygame.display.update()
        
        if playerTurn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in moveMap:
                        direction = moveMap[event.key]
                        moveList.append(direction)
                        playerPos = None
                        
                        # Find player's current position
                        for row in range(len(board)):
                            for col in range(len(board[0])):
                                if board[row][col] == 'A':
                                    playerPos = [row, col]
                        
                        # Move the player
                        playerPos = handlePlayerMovement(board,playerPos)
                        playerMoved = True
                        playerTurn = False  # End player's turn, switch to enemy turn

        # Handle enemy movement (if player's move is completed)
        if not playerTurn and playerMoved:
            monsterRemove(board, ogres, demons)
            # Move enemies
            newOgre = []
            for ogreP in ogres:
                newOgrePos = ogreMash(board, ogreP, playerPos, rows, columns)
                if newOgrePos is not None:
                    newOgre.append(newOgrePos)
                else:
                    newOgre.append(ogreP)
            ogres = newOgre

            newDemon = []
            for demonP in demons:
                newDemonPos = demonMash(board, demonP, playerPos, rows, columns)
                if newDemonPos is not None:
                    newDemon.append(newDemonPos)
                else:
                    newDemon.append(demonP)
            demons = newDemon

            # Re-add monsters and handle collisions
            monsterAdd(board, ogres, demons)
            ogreCount, demonCount = enemyCounter(board)
            score = monsterCollideCheck(ogres, demons, board, playerPos, corpses, score)

            # Check game-over conditions (player killed by demon or ogre)
            if playerPos in demons or playerPos in ogres or playerPos in corpses:
                gameOver = True
                score = 0
                playerWon = False
                
            if ogreCount == 0 and demonCount == 0:
                gameOver = True
                playerWon = True

            playerMoved = False
            playerTurn = True  # End enemy's turn, switch back to player's turn
            
            drawBoard(board)
                        
            pygame.display.update()
            clock.tick(60)
        if gameOver:
            result = "Win!" if playerWon else "Lose!"
            displayGameOver(score, result)
            running = False
            print(f"Score: {score}   MoveList: {moveList}")

    pygame.quit()

if __name__ == "__main__":
    main()
