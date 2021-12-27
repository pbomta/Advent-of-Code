#include <fstream>
#include <string>
#include <iostream>

using namespace std;

class Seafloor {
 public:
  string seafloor_;
  int width_ = 0;
  int height_ = 0;

  char Get(int r, int c) const {
    return seafloor_[r*width_ + c];
  }

  void Set(int r, int c, char x) {
    seafloor_[r*width_ + c] = x;
  }

  Seafloor MoveEasteners() const {
    Seafloor result = *this;
    for (int r = 0; r < height_; ++r) {
      for (int c = 0; c < width_; ++c) {
        if (Get(r, c) == '>') {
          auto c2 = (c + 1) % width_;
          if (Get(r, c2) == '.') {
            result.Set(r, c, '.');
            result.Set(r, c2, '>');
          }
        }
      }
    }
    return result;
  }

  Seafloor MoveSoutheners() const {
    Seafloor result = *this;
    for (int r = 0; r < height_; ++r) {
      for (int c = 0; c < width_; ++c) {
        if (Get(r, c) == 'v') {
          auto r2 = (r + 1) % height_;
          if (Get(r2, c) == '.') {
            result.Set(r, c, '.');
            result.Set(r2, c, 'v');
          }
        }
      }
    }
    return result;
  }

};

Seafloor ReadFromFile(std::string file_name) {
  auto file = ifstream(file_name);
  Seafloor result;
  while (!file.eof()) {
    string row;
    getline(file, row);
    result.seafloor_ += row;
    result.width_ = row.size();
    result.height_ += 1;
  }
  return result;
}

int main() {
  auto seafloor = ReadFromFile("2021_25_input");

  Seafloor prev_seafloor;
  int step = 0;
  while (prev_seafloor.seafloor_ != seafloor.seafloor_) {
    ++step;
    cout << step << endl;

    prev_seafloor.seafloor_ = seafloor.seafloor_;
    seafloor = seafloor.MoveEasteners().MoveSoutheners();
  }
}