//nome 
//idade
package com.example.projeto.model;
import javax.annotation.processing.Generated;

import jakarta.persistenc.Entity;
import jakarta.persistenc.Tabel;
import jakarta.persistenc.Id;
import jakarta.persistenc.GeneratedValue;
import jakarta.persistenc.GeneratedType;



@Entity
@Table(name="pessoas")
public class Pessoa{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String nome;
    private Integer idade;

    public Pessoa(){
        this("",0);
    }

    public Pessoa(String nome, Integer idade){
        this.nome = nome;
        this.idade = idade;
    }
    
    public void setNome(String nome){
        this.nome = nome;
    }
    public String getNome(){
        return this.nome;
    }
    
    public void setIdade(Integer idade){
        this.idade = idade;
    }
    public Integer getIdade(){
        return this.idade;
    }




}