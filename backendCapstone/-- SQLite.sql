-- SQLite
CREATE TABLE admin(
    AdminID integer not null PRIMARY KEY AUTOINCREMENT,
    Email text not NULL,
    Password text not NULL
);

CREATE TABLE Capstone_course(
    CourseID integer not null PRIMARY KEY AUTOINCREMENT,
    College text not null,
    Course text not null,
    AvgGrade integer not null,
    AvgCet integer not null,
    TotalScore integer not null,
    CourseDescripition text not null
);