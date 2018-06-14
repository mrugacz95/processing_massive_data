#include <iostream>
#include<fstream>
#include <vector>
#include <sstream>
#include <set>
#include <map>
#include <algorithm>
#include <iomanip>
#include <chrono>
#include <unordered_map>

using namespace std;

vector<string> split(const string &s, char delimiter) {
    vector<string> tokens;
    string token;
    istringstream tokenStream(s);
    while (getline(tokenStream, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

void insert(unordered_map<int, set<int> *> &hashmap, int key, int value) {
    auto it = hashmap.find(key);
    if (it == hashmap.end()) {
        it = hashmap.insert(make_pair(key, new set<int>)).first;
    }
    it->second->insert(value);
}

struct Counter {
    struct value_type {
        template<typename T>
        value_type(const T &) {}
    };

    void push_back(const value_type &) { ++count; }

    size_t count = 0;
};

template<typename T1, typename T2>
size_t intersection_size(const T1 &s1, const T2 &s2) {
    Counter c;
    set_intersection(s1.begin(), s1.end(), s2.begin(), s2.end(), std::back_inserter(c));
    return c.count;
}

template<typename T1, typename T2>
size_t union_size(const T1 &s1, const T2 &s2) {
    Counter c;
    set_union(s1.begin(), s1.end(), s2.begin(), s2.end(), std::back_inserter(c));
    return c.count;
}

float jaccard(set<int> *a, set<int> *b) {
    float intersec_elems = intersection_size(*a, *b);
    float union_elems = union_size(*a, *b);
    return intersec_elems / union_elems;
}

struct UsersPair {
    int u1, u2;

    bool operator==(const UsersPair &other) const {
        return u1 == other.u1 && u2 == other.u2;
    }
};

namespace std {

    template<>
    struct hash<UsersPair> {
        std::size_t operator()(const UsersPair &k) const {
            using std::size_t;
            using std::hash;

            return (hash<int>()(k.u1))
                   ^ (hash<int>()(k.u2));
        }
    };

}

int main() {
    std::ios::sync_with_stdio(false);
    string path = "../../data/facts2.csv";
    string results = "../results.txt";
    fstream file(path);
    if (!file.good()) {
        cout << "Not good.";
    }
    ofstream output(results);
    output << std::fixed << std::setprecision(3);
    if (!file.good()) {
        cout << "Output not good.";
    }
    string line;
    file >> line;

    unordered_map<int, set<int> *> users;
    unordered_map<int, set<int> *> songs;
    unordered_map<UsersPair, int> common;
    vector<int> usersOrder;

    int count = 0;
    while (file >> line) {
//        if (count++ == 100000) {
//            break;
//        }
        vector<string> row = split(line, ',');
        int song_id = stoi(row[0]);
        int user_id = stoi(row[1]);
        if (users.find(user_id) == users.end()) {
            usersOrder.push_back(user_id);
        }
        insert(users, user_id, song_id);
        auto it = songs.find(song_id);
        if (it != songs.end()) {
            for (auto user : *it->second) {
                UsersPair up;
                if (user < user_id) {
                    up.u1 = user;
                    up.u2 = user_id;
                }
                else {
                    up.u1 = user_id;
                    up.u2 = user;
                }
                common[up]++;

            }
        }
        insert(songs, song_id, user_id);
    }
    for (auto p : common) {
        cout << p.first.u1 << " " << p.first.u2 << "=" << p.second << "\n";
    }
    file.close();
    cout << "Data read.";
    count = 0;
    auto t1 = chrono::high_resolution_clock::now();
    for (auto user_id : usersOrder) {
        if (count++ == 1000) {
            cout << "\r" << count;
        }
        output << "User = " << user_id << "\n";
        set<int> others;
        for (int song_id : *users.find(user_id)->second) {
            auto it = songs.find(song_id);
            if (it != songs.end()) {
                set<int> *listeners = (it->second);
                others.insert(listeners->begin(), listeners->end());
            }
        }
        vector<pair<float, int>> similarity;
        similarity.reserve(others.size());
        for (int other : others) {
            similarity.emplace_back(make_pair(jaccard(users.find(user_id)->second, users.find(other)->second), other));
        }
        sort(similarity.begin(), similarity.end(), greater<>());
        if (similarity.size() > 100)
            similarity.resize(100);
        for (auto sim : similarity) {
            output << sim.second << ' ' << setw(7) << sim.first << "\n";
        }
        output << "\n";
        auto t2 = chrono::high_resolution_clock::now();
        auto sec = chrono::duration_cast<chrono::seconds>(t2 - t1).count();
        auto min = chrono::duration_cast<chrono::minutes>(t2 - t1).count();
        auto hour = chrono::duration_cast<chrono::hours>(t2 - t1).count();
        auto eta = (int) (((float) sec / (float) count) * (float) (usersOrder.size() - count));
        cout << "\rtook: " << std::setw(2) << setfill('0') << hour << ":" << std::setw(2) << setfill('0') << min % 60
             << ":" << std::setw(2) << setfill('0') << sec % 60
             << " done: " << count << "/" << usersOrder.size()
             << " ETA:" << std::setw(2) << setfill('0') << eta / 3600 << ":" << eta / 60 % 60 << ":" << std::setw(2)
             << setfill('0') << eta % 60;
    }
    output.close();
    for (auto song: songs) {
        song.second->clear();
        free(song.second);
    }
    for (auto user: users) {
        user.second->clear();
        free(user.second);
    }
    return 0;
}