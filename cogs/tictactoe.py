import discord
from discord.ext import commands


class TicTacToeButton(discord.ui.View):

    def __init__(self, player1, player2):
        super().__init__(timeout=None)
        self.board = ["⬜"] * 9
        self.players = [player1, player2]
        self.turn = player1
        self.game_over = False

        # Create 9 buttons for the board
        for i in range(9):
            self.add_item(TicTacToeButtonItem(i))

    async def update_board(self, interaction: discord.Interaction):
        """Update the board message after a move"""
        if self.game_over:
            return

        winner = self.check_winner()
        if winner:
            self.game_over = True
            await interaction.response.edit_message(
                content=f"{self.format_board()}\n{winner.mention} wins! 🎉",
                view=None)
            return
        elif "⬜" not in self.board:
            self.game_over = True
            await interaction.response.edit_message(
                content=f"{self.format_board()}\nIt's a tie! 🤝", view=None)
            return

        # Switch turn
        self.turn = self.players[0] if self.turn == self.players[
            1] else self.players[1]
        await interaction.response.edit_message(
            content=
            f"{self.format_board()}\n{self.turn.mention}, it's your turn!",
            view=self)

    def format_board(self):
        return "".join(self.board[i] for i in range(0, 3)) + "\n" + \
               "".join(self.board[i] for i in range(3, 6)) + "\n" + \
               "".join(self.board[i] for i in range(6, 9))

    def check_winner(self):
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
            if self.board[w[0]] != "⬜" and self.board[w[0]] == self.board[
                    w[1]] == self.board[w[2]]:
                return self.turn
        return None


class TicTacToeButtonItem(discord.ui.Button):

    def __init__(self, index):
        super().__init__(style=discord.ButtonStyle.secondary,
                         label="⬜",
                         row=index // 3)
        self.index = index

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeButton = self.view
        if interaction.user != view.turn:
            await interaction.response.send_message("It's not your turn!",
                                                    ephemeral=True)
            return
        if view.board[self.index] != "⬜":
            await interaction.response.send_message(
                "That spot is already taken!", ephemeral=True)
            return

        # Place mark
        view.board[
            self.index] = "❌" if interaction.user == view.players[0] else "⭕"
        self.label = view.board[self.index]
        self.disabled = True

        await view.update_board(interaction)


class TicTacToeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tictactoe(self, ctx, opponent: discord.Member):
        """Start a Tic Tac Toe game with buttons"""
        if opponent.bot or opponent == ctx.author:
            await ctx.send("Choose a real user other than yourself!")
            return

        view = TicTacToeButton(ctx.author, opponent)
        await ctx.send(
            f"Tic Tac Toe started! {ctx.author.mention} (❌) vs {opponent.mention} (⭕)\n{ctx.author.mention}, it's your turn!",
            view=view)


def setup(bot):
    bot.add_cog(TicTacToeCog(bot))
