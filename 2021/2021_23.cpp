#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <optional>
#include <unordered_set>
#include <string>

constexpr auto kNrBurrows = 4;
constexpr auto kNumToChar = "0123";
constexpr std::array<int, kNrBurrows> kBurrowsPos = {2, 4, 6, 8};

constexpr int ctoi(char c) {
    return static_cast<int>(c) - '0';
}

constexpr auto kAmphNumToName = "ABCD";
constexpr char AmphName(char aa) {
  return kAmphNumToName[ctoi(aa)];
}

template <int tBurrowDepth>
class Burrow {
  public:
    Burrow(std::string hallway, std::array<std::string, kNrBurrows> burrows)
      : hallway_{std::move(hallway)}
      , burrows_{std::move(burrows)}
      , energy_usage_{0} {
    }

    bool IsDone() const {
        for (int n = 0; n < kNrBurrows; ++n)
            if (std::count(burrows_[n].begin(), burrows_[n].end(), kNumToChar[n]) != tBurrowDepth) {
                return false;
            }
        return true;
    }

    bool Equivalent(Burrow const& other) const {
      return hallway_ == other.hallway_ && burrows_ == other.burrows_;
    }

    long long Score() const {
      long long result = 0;
      for (int b = 0; b < kNrBurrows; ++b) {
        for (char bb : burrows_[b]) {
          if (bb == kNumToChar[b]) {
            result += 10000;
          } else {
            result -= 5000;
          }
        }
      }
      return result;
    }

    std::optional<Burrow> MoveToBurrow(int pos) const {
      if (hallway_[pos] == '.') {
          return {};
      }

      int a = ctoi(hallway_[pos]);
      if (burrows_[a].size() == tBurrowDepth) {
          return {}; // No room
      }

      char aa = kNumToChar[a];
      if (std::any_of(burrows_[a].begin(), burrows_[a].end(), [aa](char c) { return c != aa; })) {
        return {}; // Wrong anthropods in there
      }

      // Check path
      int steps = 1 + tBurrowDepth - burrows_[a].size(); // One initial step, plus depth into burrow
      int inc = kBurrowsPos[a] > pos ? 1 : -1;
      for (int p = pos + inc; p != kBurrowsPos[a]; p += inc) {
          ++steps;
          if (hallway_[p] != '.') {
              return {}; // Blocked
          }
      }

      // Done! We can make that move.
      auto new_burrow = *this;
      new_burrow.hallway_[pos] = '.';
      new_burrow.burrows_[a].push_back(aa);
      new_burrow.energy_usage_ += steps * std::pow(10, a);
      return new_burrow;
    }

    std::vector<Burrow> MoveToHallway(int b) const {
      // b = burrow index
      if (burrows_[b].empty()) {
          return {};
      }

      char bb = kNumToChar[b];
      if (std::all_of(burrows_[b].begin(), burrows_[b].end(), [bb](char c){ return c == bb; })) {
          return {}; // Only anthropods in there that should stay there
      }

      char aa = burrows_[b].back();
      int a = ctoi(aa);
      std::vector<Burrow> result;

      int steps = 1 + tBurrowDepth - burrows_[b].size();
      for (int p = kBurrowsPos[b] + 1; p < static_cast<int>(hallway_.size()); ++p) {
          ++steps;
          if (hallway_[p] != '.') {
              break; // Blocked
          }
          if (std::count(kBurrowsPos.begin(), kBurrowsPos.end(), p) > 0) {
              continue; // Move beyond burrow exits
          }

          auto new_burrow = *this;
          new_burrow.hallway_[p] = aa;
          new_burrow.burrows_[b].pop_back();
          new_burrow.energy_usage_ += steps * std::pow(10, a);
          result.push_back(new_burrow);
      }

      steps = 1 + tBurrowDepth - burrows_[b].size();
      for (int p = kBurrowsPos[b] - 1; p >= 0; --p) {
          ++steps;
          if (hallway_[p] != '.') {
              break; // Blocked
          }
          if (std::count(kBurrowsPos.begin(), kBurrowsPos.end(), p) > 0) {
              continue; // Move beyond burrow exits
          }

          auto new_burrow = *this;
          new_burrow.hallway_[p] = aa;
          new_burrow.burrows_[b].pop_back();
          new_burrow.energy_usage_ += steps * std::pow(10, a);
          result.push_back(new_burrow);
      }

      return result;
    }

    std::vector<Burrow> Possibilities() const {
      std::vector<Burrow> result;
      for (int b = 0; b < kNrBurrows; ++b) {
          auto options = MoveToHallway(b);
          for (const auto& option : options) {
            result.push_back(option);  
          }
      }
      for (int p = 0; p < static_cast<int>(hallway_.size()); ++p) {
        auto option = MoveToBurrow(p);
        if (option) {
            result.push_back(*option);
        }
      }
      return result;
    }

    std::string hallway_;
    std::array<std::string, kNrBurrows> burrows_;
    long long energy_usage_;
};

template <int T>
std::ostream& operator<<(std::ostream& o, Burrow<T> const& B) {
  for (auto c : B.hallway_) {
    if (c == '.')
      o << c;
    else
      o << AmphName(c);
  }
  o << "\n";
  for (int n = T - 1; n >= 0; --n) {
    o << "  ";
    for (int b = 0; b < kNrBurrows; ++b) {
      if (static_cast<int>(B.burrows_[b].size()) > n) {
        o << AmphName(B.burrows_[b][n]) << " ";
      }
      else {
        o << "  ";
      }
    }
    o << " \n";
  }
  return o;
}

void UnitTests() {
  auto Btest0 = Burrow<2>("...........", {"01", "32", "21", "03"});
  auto Btest0_next = Btest0.MoveToHallway(2);
  // for (auto const& B : Btest0_next) {
  //   std::cout << B;
  // }
  auto Btest1 = Btest0_next[4];
  if (Btest1.energy_usage_ != 40) {
    
    std::cout << "Btest1.energy_usage_ 40 != " << Btest1.energy_usage_;
    exit(1);
  }
  if (!Btest1.MoveToHallway(2).empty()) {
    std::cout << "Error";
    exit(1);
  }
  auto Btest1_next = Btest1.MoveToHallway(1);
  // for (auto const& B : Btest1_next) {
  //   std::cout << B;
  // }
  auto Btest2 = Btest1_next[0].MoveToBurrow(5);
  if (!Btest2) {
    std::cout << "Error";
    exit(1);
  }
  if (Btest2->energy_usage_ != 440) {
    
    std::cout << "Btest2.energy_usage_ 440 != " << Btest2->energy_usage_;
    exit(1);
  }
  if (!Btest2->MoveToHallway(2).empty()) {
    std::cout << "Error";
    exit(1);
  }
}

template <int T>
struct BurrowHash {
  constexpr std::size_t operator()(Burrow<T> const& burrow) const {
    std::size_t result = 0;
    for (int n = 0; n < static_cast<int>(burrow.hallway_.size()); ++n) {
      result += n*burrow.hallway_[n];
    }
    for (int b = 0; b < kNrBurrows; ++b) {
      result *= std::hash<std::string>()(burrow.burrows_[b]);
    }
    return result;
  }
};

template <int T>
struct BurrowEqual {
  constexpr bool operator()(Burrow<T> const& lhs, Burrow<T> const& rhs) const 
  {
    return lhs.hallway_ == rhs.hallway_ && lhs.burrows_ == rhs.burrows_;
  }
};

int main()
{
  UnitTests();

  // Testcase. Costs 12521 energy
  // auto B_input = Burrow<2>("...........", {"01", "32", "21", "03"});

// Part 2 input. optimal < 55138
// ...........
//   C A B D
//   D C B A 
//   D B A C 
//   C A D B
  auto B_input = Burrow<4>("...........", {"2332", "0120", "3011", "1203"});
  std::vector<Burrow<4>> frontier = {B_input};
  std::unordered_set<
    Burrow<4>,
    BurrowHash<4>,
    BurrowEqual<4>
    > visited;
  long long optimal = std::numeric_limits<long long>::max();
  long long n = 0;
  while (!frontier.empty()) {
    ++n;

    // Consider the next one
    auto best_candidate = std::min_element(frontier.begin(), frontier.end(), [](auto const& lhs, auto const& rhs){
      return lhs.energy_usage_ < rhs.energy_usage_;
    });
    auto [next_burrow, is_new] = visited.insert(*best_candidate);
    frontier.erase(best_candidate);
    if (!is_new) {
      continue;
    }

    if (n % 1000 == 0) {
      std::cout << "\nOptimum: " << optimal << " Checked: " << visited.size() << " Work: " << frontier.size() << " Up next: \n";
      std::cout << *next_burrow;
    }

    // Propagate into new states
    auto next_states = next_burrow->Possibilities();
    for (auto const& s : next_states) {
      if (s.energy_usage_ >= optimal) {
        continue;
      } else if (s.IsDone()) {
        if (s.energy_usage_ < optimal) {
          optimal = s.energy_usage_;
          // std::cout << "Lowest energy so far: " << optimal << " checked: " << visited.size() << "\n";
        }
      } else if(auto it = visited.find(s); it != visited.end()) {
        continue;
      } else {
        frontier.push_back(s);
      }
    }
  }

  std::cout << "Finished! The optimal solution expends " << optimal << " energy.\n";
}