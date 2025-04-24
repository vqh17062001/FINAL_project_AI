import time
import numpy as np
import matplotlib.pyplot as plt
import os

class GameAnalytics:
    """
    Class for tracking performance metrics of agents in games.
    """
    
    def __init__(self):
        """Initialize analytics."""
        self.results = {
            'wins': {},
            'total_games': 0,
            'times': {},
            'memory': {},
        }
    
    def record_game_result(self, winner, agents):
        """
        Record the result of a game.
        
        Args:
            winner: The winning agent's color (or 0 for draw)
            agents: List of agents that played
        """
        self.results['total_games'] += 1
        
        # Record win for the winning agent
        for agent in agents:
            # Initialize if this is the first game for this agent
            if agent.name not in self.results['wins']:
                self.results['wins'][agent.name] = 0
                self.results['times'][agent.name] = []
                self.results['memory'][agent.name] = []
            
            # Record win if this agent won
            if winner == agent.color:
                self.results['wins'][agent.name] += 1
            
            # Record time and memory metrics
            self.results['times'][agent.name].append(agent.get_average_time())
            self.results['memory'][agent.name].append(agent.get_average_memory())
    
    def get_win_rates(self):
        """
        Get the win rates for each agent.
        
        Returns:
            dict: Win rates for each agent
        """
        win_rates = {}
        for agent_name, wins in self.results['wins'].items():
            win_rates[agent_name] = wins / self.results['total_games']
        return win_rates
    
    def get_average_times(self):
        """
        Get the average time per move for each agent.
        
        Returns:
            dict: Average times for each agent
        """
        avg_times = {}
        for agent_name, times in self.results['times'].items():
            avg_times[agent_name] = np.mean(times)
        return avg_times
    
    def get_average_memory(self):
        """
        Get the average memory usage per move for each agent.
        
        Returns:
            dict: Average memory usage for each agent
        """
        avg_memory = {}
        for agent_name, memory in self.results['memory'].items():
            avg_memory[agent_name] = np.mean(memory)
        return avg_memory
    
    def print_summary(self):
        """Print a summary of the analytics."""
        print("\n=== Game Analytics Summary ===")
        print(f"Total Games: {self.results['total_games']}")
        print("\nWin Rates:")
        win_rates = self.get_win_rates()
        for agent_name, win_rate in win_rates.items():
            wins = self.results['wins'][agent_name]
            print(f"  {agent_name}: {win_rate:.2%} ({wins}/{self.results['total_games']})")
        
        print("\nAverage Time per Move:")
        avg_times = self.get_average_times()
        for agent_name, avg_time in avg_times.items():
            print(f"  {agent_name}: {avg_time:.4f} seconds")
        
        print("\nAverage Memory Usage per Move:")
        avg_memory = self.get_average_memory()
        for agent_name, memory in avg_memory.items():
            print(f"  {agent_name}: {memory:.2f} MB")
    
    def plot_metrics(self, save_dir=None):
        """
        Plot analytics metrics.
        
        Args:
            save_dir (str, optional): Directory to save plots. If None, plots are displayed.
        """
        # Create save directory if needed
        if save_dir is not None:
            os.makedirs(save_dir, exist_ok=True)
        
        # Plot win rates
        self._plot_win_rates(save_dir)
        
        # Plot average times
        self._plot_average_times(save_dir)
        
        # Plot average memory usage
        self._plot_average_memory(save_dir)
    
    def _plot_win_rates(self, save_dir=None):
        """Plot win rates for each agent."""
        win_rates = self.get_win_rates()
        
        plt.figure(figsize=(10, 6))
        plt.bar(win_rates.keys(), win_rates.values())
        plt.title('Agent Win Rates')
        plt.xlabel('Agent')
        plt.ylabel('Win Rate')
        plt.ylim(0, 1)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add win rate values on top of bars
        for i, (agent, rate) in enumerate(win_rates.items()):
            plt.text(i, rate + 0.02, f'{rate:.2%}', ha='center')
        
        if save_dir:
            plt.savefig(os.path.join(save_dir, 'win_rates.png'))
            plt.close()
        else:
            plt.show()
    
    def _plot_average_times(self, save_dir=None):
        """Plot average time per move for each agent."""
        avg_times = self.get_average_times()
        
        plt.figure(figsize=(10, 6))
        plt.bar(avg_times.keys(), avg_times.values())
        plt.title('Average Time per Move')
        plt.xlabel('Agent')
        plt.ylabel('Time (seconds)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add time values on top of bars
        for i, (agent, time) in enumerate(avg_times.items()):
            plt.text(i, time + 0.0005, f'{time:.4f}s', ha='center')
        
        if save_dir:
            plt.savefig(os.path.join(save_dir, 'average_times.png'))
            plt.close()
        else:
            plt.show()
    
    def _plot_average_memory(self, save_dir=None):
        """Plot average memory usage per move for each agent."""
        avg_memory = self.get_average_memory()
        
        plt.figure(figsize=(10, 6))
        plt.bar(avg_memory.keys(), avg_memory.values())
        plt.title('Average Memory Usage per Move')
        plt.xlabel('Agent')
        plt.ylabel('Memory (MB)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add memory values on top of bars
        for i, (agent, mem) in enumerate(avg_memory.items()):
            plt.text(i, mem + 0.05, f'{mem:.2f} MB', ha='center')
        
        if save_dir:
            plt.savefig(os.path.join(save_dir, 'average_memory.png'))
            plt.close()
        else:
            plt.show()
    
    def reset(self):
        """Reset analytics."""
        self.results = {
            'wins': {},
            'total_games': 0,
            'times': {},
            'memory': {},
        }