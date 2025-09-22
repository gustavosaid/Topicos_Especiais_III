CREATE TABLE aluno(
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL
)

insert INTO aluno (nome,idade) VALUES ('Adriana', 51)

select * from aluno