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

void printTime(chrono::high_resolution_clock::time_point point, int count, int size) {
    auto t2 = chrono::high_resolution_clock::now();
    auto sec = chrono::duration_cast<chrono::seconds>(t2 - point).count();
    auto min = chrono::duration_cast<chrono::minutes>(t2 - point).count();
    auto hour = chrono::duration_cast<chrono::hours>(t2 - point).count();
    auto eta = (int) (((float) sec / (float) count) * (float) (size - count));
    cout << "\rtook: " << std::setw(2) << setfill('0') << hour << ":" << std::setw(2) << setfill('0') << min % 60
         << ":" << std::setw(2) << setfill('0') << sec % 60
         << " done: " << count << "/" << size
         << " ETA:" << std::setw(2) << setfill('0') << eta / 3600 << ":" << std::setw(2) << setfill('0')
         << eta / 60 % 60 << ":" << std::setw(2) << setfill('0') << eta % 60;
}

vector<string> split(const string &s, char delimiter) {
    vector<string> tokens;
    string token;
    istringstream tokenStream(s);
    while (getline(tokenStream, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

void insert(unordered_map<int, set<int>> &hashmap, int key, int value) {
    auto it = hashmap.find(key);
    if (it == hashmap.end()) {
        set<int> s;
        it = hashmap.insert(make_pair(key, s)).first;
    }
    it->second.insert(value);
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

UsersPair makeUserPair(int user1, int user2) {
    UsersPair up;
    if (user1 < user2)
        up = {user1, user2};
    else
        up = {user2, user2};
    return up;
}

float
count_jaccard(unordered_map<UsersPair, int> &common, int user1, int user2, unordered_map<int, set<int>> &users) {
    if (user1 == user2) {
        return 1.0;
    }
    UsersPair up = makeUserPair(user1, user2);
    float commonCount = common[up];
    return commonCount / (users.find(user1)->second.size() + users.find(user2)->second.size() - commonCount);
}


unordered_map<int, set<int>> users;
unordered_map<int, set<int>> songs;
unordered_map<UsersPair, int> common;
vector<int> usersOrder;

int main() {
//    std::ios::sync_with_stdio(false);
    string path = "../../data/facts.csv";
    string results = "../results_cpp.txt";
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


    int count = 0;
    auto t1 = chrono::high_resolution_clock::now();
    while (file >> line) {
//        if (count++ == 100000) {
//            break;
//        }
        count++;
        vector<string> row = split(line, ',');
        int song_id = stoi(row[0]);
        int user_id = stoi(row[1]);
        if (users.find(user_id) == users.end()) {
            usersOrder.push_back(user_id);
        }
        insert(users, user_id, song_id);
        auto it = songs.find(song_id);
        if (it != songs.end()) {
            for (auto user : it->second) {
                UsersPair up = makeUserPair(user, user_id);
                common[up]++;
            }
        }
        insert(songs, song_id, user_id);
        if(count % 10000 == 0)
            printTime(t1, count, 27729358);
    }
//    for (auto p : common) {
//        cout << p.first.u1 << " " << p.first.u2 << "=" << p.second << "\n";
//    }
    file.close();
    cout << "Data read.";
    count = 0;
    t1 = chrono::high_resolution_clock::now();
    for (auto user_id : usersOrder) {
        if (count++ == 100) {
            break;
//            cout << "\r" << count;
        }
        output << "User = " << user_id << "\n";
        set<int> others;
        for (int song_id : users.find(user_id)->second) {
            auto it = songs.find(song_id);
            if (it != songs.end()) {
                set<int> listeners = (it->second);
                others.insert(listeners.begin(), listeners.end());
            }
        }
        vector<pair<float, int>> similarity;
        similarity.reserve(others.size());
        for (int other : others) {
//            similarity.emplace_back(make_pair(jaccard(users.find(user_id)->second, users.find(other)->second), other));
            similarity.emplace_back(make_pair(count_jaccard(common, user_id, other, users), other));
        }
        sort(similarity.begin(), similarity.end(), greater<>());
        if (similarity.size() > 100)
            similarity.resize(100);
        for (auto sim : similarity) {
            output << setw(8) << sim.second << 'x' << setw(7) << sim.first << "\n";
        }
        output << "\n";
        printTime(t1, count, users.size());
    }
    output.close();
    return 0;
}
