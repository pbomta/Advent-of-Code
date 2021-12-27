#include <algorithm>
#include <iostream>
#include <array>

using namespace std;

class DetDie100 {
 public:
  int Roll() {
    ++rolled_;
    return next_++;
  }

  int next_ = 1;
  int rolled_ = 0;
};

class Universe {
 public:
  // Player 1 starting position: 1
  // Player 2 starting position: 6
  array<int, 2> player_pos = {1, 6}; // Real input
  // array<int, 2> player_pos = {4, 8}; // Test input
  array<int, 2> player_score = {0, 0};

  int active_player = 0;

  long long multiplier = 1; // How many similar universes exist
};

std::array<int, 10> kMultipliers = {0, 0, 0, 1, 3, 6, 7, 6, 3, 1};

int main() {
  int player1_pos = 1;
  int player1_score = 0;
  int player2_pos = 6;
  int player2_score = 0;

  auto die = DetDie100();
  while (true) {
    player1_pos += die.Roll() + die.Roll() + die.Roll();
    player1_pos = 1 + (player1_pos - 1) % 10;
    player1_score += player1_pos;
    if (player1_score >= 1000)
      break;

    player2_pos += die.Roll() + die.Roll() + die.Roll();
    player2_pos = 1 + (player2_pos - 1) % 10;
    player2_score += player2_pos;
    if (player2_score >= 1000)
      break;
  }

  cout << "Practice game: " << min(player1_score, player2_score) * die.rolled_ << endl;

  constexpr int kWinningScore = 21;

  vector<Universe> multiverse{Universe()};
  vector<Universe> finished;
  while (!multiverse.empty()) {
    cout << multiverse.size() << endl;
    vector<Universe> next_multiverse;
    for (const Universe& u : multiverse) {
      for (int k = 3; k <= 9; ++k) {
        Universe new_universe = u;
        int& pos = new_universe.player_pos[new_universe.active_player];
        int& score = new_universe.player_score[new_universe.active_player];
        pos = 1 + (pos + k - 1) % 10;
        score += pos;
        new_universe.active_player = (new_universe.active_player == 1 ? 0 : 1);
        new_universe.multiplier *= kMultipliers[k];
        if (score >= kWinningScore)
          finished.push_back(new_universe);
        else
          next_multiverse.push_back(new_universe);
      }
    }
    multiverse = std::move(next_multiverse);
  }

  long long player1_wins = 0, player2_wins = 0;
  for (const auto& u : finished) {
    if (u.player_score[0] >= kWinningScore)
      player1_wins += u.multiplier;
    else
      player2_wins += u.multiplier;
  }

  cout << "Dirac game, player 1 wins: " << player1_wins << ", player 2 wins: " << player2_wins << endl;
}