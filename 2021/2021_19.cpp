#include <array>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <iostream>
#include <limits>
#include <tuple>
#include <vector>
#include <map>

using namespace std;

constexpr auto kScanRange = 1000;
constexpr auto kNrRotations = 24;

struct Point {
    int x;
    int y;
    int z;
};

constexpr bool operator==(Point a, Point b) {
  return a.x == b.x && a.y == b.y && a.z == b.z;
}

constexpr bool operator!=(Point a, Point b) {
  return !operator==(a, b);
}

std::ostream& operator<<(std::ostream& o, Point p) {
  o << "(" << p.x << "," << p.y << "," << p.z << ")";
  return o;
}

// Rotation functions around 0
constexpr Point Rotate90XAxis(Point p) {
  return Point{p.x, -p.z, p.y};
}
constexpr Point Rotate90YAxis(Point p) {
  return Point{p.z, p.y, -p.x};
}
constexpr Point Rotate270YAxis(Point p) {
  return Point{-p.z, p.y, p.x};
}

std::vector<Point> RotationPermutations(Point p) {
  std::vector<Point> result;
  result.reserve(kNrRotations);
  for (int rx = 0; rx < 6; ++rx) {
    p = Rotate90XAxis(p);
    result.push_back(p);
    for (int ry = 0; ry < 3; ++ry) {
      if (rx % 2 == 0) {
        p = Rotate90YAxis(p);
      } else {
        p = Rotate270YAxis(p);
      }
      result.push_back(p);
    }
  }
  return result;
}

class Scanner {
  public:
    Scanner() = default;

    void AddBeacon(Point p) { beacons_.push_back(p); }

    std::array<Scanner, kNrRotations> RotationPermutations() const {
      std::array<Scanner, kNrRotations> result;
      for (auto p : beacons_) {
        auto rotated = ::RotationPermutations(p);
        for (int r = 0; r < kNrRotations; ++r) {
          result[r].AddBeacon(rotated[r]);
        }
      }
      return result;
    }

    std::vector<Point> beacons_;
};

std::ostream& operator<<(std::ostream& o, Scanner const& s) {
  o << "--- scanner ---\n";
  for (auto p : s.beacons_) 
    o << p << "\n";
  return o;
}

class Map {
  public:
    Map() = default;

    Map(Scanner const& initial_input) : scanners_{}, beacons_{initial_input.beacons_} {
      scanners_.push_back(Point{0, 0, 0});
    }

    tuple<int, int, int, int> Fit(Scanner const& s) {
      // Calculate all possible options for a fit and their occurrences
      map<tuple<int, int, int>, int> permutations;
      for (const auto p_map : beacons_) {
        for (const auto p_s : s.beacons_) {
          int dx = p_map.x - p_s.x;
          int dy = p_map.y - p_s.y;
          int dz = p_map.z - p_s.z;
          permutations[{dx, dy, dz}] += 1;
        }
      }

      // Pick the best one
      while(!permutations.empty()) {
        auto it = max_element(permutations.begin(), permutations.end(), [](auto lhs, auto rhs){
          return lhs.second < rhs.second; // Occurrence of the permutation. More points is more better! :)
        });
        // cout << "trying [" << get<0>(it->first) << "," << get<1>(it->first) << "," << get<2>(it->first) << "] fits " << it->second << " beacons.\n";
        if (it->second < 2) {
          break; // Only one beacon, not a chance.
        }
        // FIXME: This does not seem to be needed. The best permutation always wins anyway, so invalid ones are just not chosen.
        auto score = FitScore(s, get<0>(it->first), get<1>(it->first), get<2>(it->first));
        if (score) {
          tuple<int, int, int, int> best = {get<0>(it->first), get<1>(it->first), get<2>(it->first), score};
          cout << "translation [" << get<0>(best) << "," << get<1>(best) << "," << get<2>(best) << "] fits " << get<3>(best) << " beacons.\n";
          return best;
        } else {
          // It's no good. Remove that option.
          permutations.erase(it);
        }
      }
      return {0, 0, 0, 0};
    }

    int FitScore(Scanner const& s, int dx, int dy, int dz) {
      int score = 0;
      for (auto p : s.beacons_) {
        auto tp = Point{p.x + dx, p.y + dy, p.z + dz};
        if (std::any_of(scanners_.begin(), scanners_.end(), [tp](Point s) {
          return abs(s.x - tp.x) <= kScanRange && abs(s.y - tp.y) <= kScanRange && abs(s.z - tp.z) <= kScanRange;
        })) {
          if (std::find(beacons_.begin(), beacons_.end(), tp) == beacons_.end()) {
            // Didn't find this beacon, whereas it is in range of the known scanners. Conflict.
            // cout << "Discarding...\n";
            return 0;
          }
          ++score;
        }
      }
      return score;
    }

    void AddScanner(Scanner const& s, int dx, int dy, int dz) {
      scanners_.push_back({dx, dy, dz});
      for (auto p : s.beacons_) {
        Point new_beacon{p.x + dx, p.y + dy, p.z + dz};
        if (count(beacons_.begin(), beacons_.end(), new_beacon) == 0) {
          beacons_.push_back(new_beacon);
        }
      }
    }

    std::vector<Point> scanners_; // For the scanrange
    std::vector<Point> beacons_;
};

std::ostream& operator<<(std::ostream& o, Map const& m) {
  o << "--- map, beacons ---\n";
  for (auto p : m.beacons_) 
    o << p << "\n";
  return o;
}


std::vector<Scanner> ReadInputFile(std::string const& input_file_name) {
  std::vector<Scanner> scanners;
  // cout << "Parsing scanners: ";

  FILE* input_file = fopen(input_file_name.c_str(), "r");
  char buffer[256];
  while (buffer[0] != 'e') {
    Scanner new_scanner;
    fgets(buffer, 256, input_file);
    while(true) {
      Point p;
      fgets(buffer, 256, input_file);
      if (buffer[0] == 'e' || buffer[0] == '\n')
        break;
      sscanf(buffer, "%d,%d,%d", &p.x, &p.y, &p.z);
      new_scanner.AddBeacon(p);
    }
    scanners.push_back(new_scanner);
  }

  fclose(input_file);

  return scanners;
}

void UnitTestPointRotation() {
  // RotationPermutations
  auto p = Point{1, 2, 3};
  auto permutations = RotationPermutations(p);
  if (permutations[23] != Point{ 1,  2,  3}) exit(1); //   0,   0,   0
  if (permutations[22] != Point{ 3,  2, -1}) exit(1); //   0,  90,   0 |  90, 90,  90
  if (permutations[21] != Point{-1,  2, -3}) exit(1); //   0, 180,   0 | 180,  0, 180
  if (permutations[20] != Point{-3,  2,  1}) exit(1); //   0, 270,   0
  if (permutations[ 0] != Point{ 1, -3,  2}) exit(1); //  90,   0,   0 
  if (permutations[ 1] != Point{ 2, -3, -1}) exit(1); //  90,  90,   0 |   0, 90, 270
  if (permutations[ 2] != Point{-1, -3, -2}) exit(1); //  90, 180,   0 | 270,  0, 180
  if (permutations[ 3] != Point{-2, -3,  1}) exit(1); //  90, 270,   0
  if (permutations[11] != Point{ 1, -2, -3}) exit(1); // 180,   0,   0
  if (permutations[ 8] != Point{-3, -2, -1}) exit(1); // 180,  90,   0 |   0, 90, 180
  if (permutations[ 9] != Point{-1, -2,  3}) exit(1); // 180, 180,   0 |   0,  0, 180
  if (permutations[10] != Point{ 3, -2,  1}) exit(1); // 180, 270,   0
  if (permutations[12] != Point{ 1,  3, -2}) exit(1); // 270,   0,   0
  if (permutations[15] != Point{-2,  3, -1}) exit(1); // 270,  90,   0 |   0, 90, 90
  if (permutations[14] != Point{-1,  3,  2}) exit(1); // 270, 180,   0 |  90,  0, 180
  if (permutations[13] != Point{ 2,  3,  1}) exit(1); // 270, 270,   0
  if (permutations[16] != Point{-2,  1,  3}) exit(1); //   0,   0,  90
  if (permutations[ 6] != Point{ 2, -1,  3}) exit(1); //   0,   0, 270
  if (permutations[17] != Point{ 3,  1,  2}) exit(1); //  90,   0,  90
  if (permutations[ 7] != Point{-3, -1,  2}) exit(1); //  90,   0, 270
  if (permutations[18] != Point{ 2,  1, -3}) exit(1); // 180,   0,  90
  if (permutations[ 4] != Point{-2, -1, -3}) exit(1); // 180,   0, 270
  if (permutations[19] != Point{-3,  1, -2}) exit(1); // 270,   0,  90
  if (permutations[ 5] != Point{ 3, -1, -2}) exit(1); // 270,   0, 270
  // Niet verder gekeken dan 90, 90, 90.

  cout << "UnitTestPointRotation passed\n";
}

void UnitTestFitting1() {
  Scanner s0;
  s0.AddBeacon({-618,-824,-621});
  s0.AddBeacon({-537,-823,-458});
  s0.AddBeacon({-447,-329,318});

  Scanner s1;
  s1.AddBeacon({686,422,578});
  s1.AddBeacon({605,423,415});
  s1.AddBeacon({515,917,-361});

  Map map(s0);
  auto perm1 = s1.RotationPermutations();
  size_t best_r;
  int best_dx, best_dy, best_dz, best_score = 0; 
  for (size_t r = 0; r < perm1.size(); ++r) {
    int dx, dy, dz, score;
    std::tie(dx, dy, dz, score) = map.Fit(perm1[r]);
    if (score > best_score) {
      best_r = r;
      best_dx = dx;
      best_dy = dy;
      best_dz = dz;
      best_score = score;
    }
  }
  
  if (best_score == 3) {
    cout << "Unittest1 passed with score: " << map.FitScore(perm1[best_r], best_dx, best_dy, best_dz) << "\n";
  } else {
    exit(1);
  }
}

void UnitTestFitting2() {
  auto scanners = ReadInputFile("2021_19_testcase");

  Map map(scanners[0]);
  auto perm1 = scanners[1].RotationPermutations();
  size_t best_r;
  int best_dx, best_dy, best_dz, best_score = 0; 
  for (size_t r = 0; r < perm1.size(); ++r) {
    int dx, dy, dz, score;
    std::tie(dx, dy, dz, score) = map.Fit(perm1[r]);
    if (score > best_score) {
      best_r = r;
      best_dx = dx;
      best_dy = dy;
      best_dz = dz;
      best_score = score;
    }
  }
  
  if (best_score > 0) {
    cout << "Unittest2 passed with score: " << map.FitScore(perm1[best_r], best_dx, best_dy, best_dz) << "\n";
  } else {
    exit(1);
  }
}

int main()
{
  UnitTestPointRotation();
  UnitTestFitting1();
  UnitTestFitting2();

  auto scanners = ReadInputFile("2021_19_input");

  // cout << scanners[0] << "\n\n" << scanners[1];
  // for (const auto& s : scanners)
  //   cout << s << endl;
  Map map(scanners[0]);
  scanners.erase(scanners.begin());

  cout << "Determining candidates...\n";

  vector<array<Scanner, kNrRotations>> candidates;
  for (const auto& scanner : scanners) {
    candidates.push_back(scanner.RotationPermutations());
  }

  while(!candidates.empty()) {
    cout << "Fitting candidates, " << candidates.size() << " left...\n";
    size_t best_n, best_r;
    int best_score = 0, best_dx, best_dy, best_dz;
    for (size_t n = 0; n < candidates.size(); ++n) {
      for (size_t r = 0; r < kNrRotations; ++r) {
        // cout << "Trying nr: " << n << " at rotation: " << r << std::endl;
        int dx, dy, dz, score;
        std::tie(dx, dy, dz, score) = map.Fit(candidates[n][r]);
        if (score > best_score) {
          best_score = score;
          best_n = n;
          best_r = r;
          best_dx = dx;
          best_dy = dy;
          best_dz = dz;
        }
      }
    }
    if (best_score > 1) {
      // cout << "Found a match with score: " << best_score << "\n";
      map.AddScanner(candidates[best_n][best_r], best_dx, best_dy, best_dz);
      candidates.erase(candidates.begin() + best_n);
    } else {
      cout << "Fatal error! Can't continue.\n";
      exit(1);
    }
  }

  cout << "Map composition complete! " << map.beacons_.size() << " beacons exist.\n";

  int furthest = 0;
  for (Point a : map.scanners_) {
    for (Point b : map.scanners_) {
      auto manhattan_distance = abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z);
      furthest = max(furthest, manhattan_distance);
    }
  }
  cout << "The biggest manhattan distance between 2 scanners is: " << furthest << "\n";
}