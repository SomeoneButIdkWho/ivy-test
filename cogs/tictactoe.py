import discord
from discord.ext import commands


class TicTacToe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.games = {}  # key: channel id, value: game state

    @commands.command()
    async def tictactoe(self, ctx, opponent: discord.Member):
        """Start a Tic Tac Toe game with another user"""
        if ctx.channel.id in self.games:
            await ctx.send("A game is already in progress in this channel!")
            return

        board = ["⬜"] * 9
        turn = ctx.author
        self.games[ctx.channel.id] = {
            "board": board,
            "players": [ctx.author, opponent],
            "turn": turn
        }

        await ctx.send(
            f"Tic Tac Toe started between {ctx.author.mention} (❌) and {opponent.mention} (⭕)!\n"
            f"{self.format_board(board)}\n"
            f"{turn.mention}, it's your turn! Use `i!place <position>` (1-9).")

    @commands.command()
    async def place(self, ctx, position: int):
        """Place your mark on the board"""
        if ctx.channel.id not in self.games:
            await ctx.send("No game in progress here!")
            return

        game = self.games[ctx.channel.id]
        board = game["board"]
        if ctx.author != game["turn"]:
            await ctx.send("It's not your turn!")
            return

        if position < 1 or position > 9 or board[position - 1] != "⬜":
            await ctx.send("Invalid move! Choose an empty spot from 1 to 9.")
            return

        mark = "❌" if ctx.author == game["players"][0] else "⭕"
        board[position - 1] = mark

        winner = self.check_winner(board)
        if winner:
            await ctx.send(
                f"{self.format_board(board)}\n{ctx.author.mention} wins! 🎉")
            del self.games[ctx.channel.id]
            return
        elif "⬜" not in board:
            await ctx.send(f"{self.format_board(board)}\nIt's a tie! 🤝")
            del self.games[ctx.channel.id]
            return

        # Switch turn
        game["turn"] = game["players"][0] if game["turn"] == game["players"][
            1] else game["players"][1]
        await ctx.send(
            f"{self.format_board(board)}\n{game['turn'].mention}, it's your turn!"
        )

    def format_board(self, board):
        return "\n".join(["".join(board[i:i + 3]) for i in range(0, 9, 3)])

    def check_winner(self, b):
        wins = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # rows
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # columns
            [0, 4, 8],
            [2, 4, 6]  # diagonals
        ]
        for w in wins:
            if b[w[0]] != "⬜" and b[w[0]] == b[w[1]] == b[w[2]]:
                return True
        return False


def setup(bot):
    bot.add_cog(TicTacToe(bot))
