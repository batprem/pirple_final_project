# pirple_final_project
The final project for the online Python course "Pirpie.com"

Notice:
main.py - The server file run on port 5001
client.py = The client for player to login and play

# Use case
1. Run main.py to start the server
2. Run client.py to login
  - Enter the name for example "Bob"
  - Enther the credits the player owns for example 5000
  - This will login a player. If the player is the first who login id will 0
3. The player will be passed to the lobby which can choose to challenge another player or wait for a challenger
4. In this use case type 'wait' to wait

5. Run client.py to login another player
  - Enter the name and the credits again for example "Bane" and 4500
  - If the player is the secind who login id will be 1
6. This id and name of "Bob" will appear to the lobby board
7. As Bane, type Bob's id, 0, to challenge Bob
8. On Bob screen will show the challenge from Bane
9. Enter Bane's id, 1, to accept his challenge
10. Bob will start first, do an action
11. Then, it's Bane's turn
12. After, Bane's turn score will be calculated and the winner will be shown
13. Both players will be forwarded to the lobby
