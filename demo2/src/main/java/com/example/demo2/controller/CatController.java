package com.example.demo2.controller;

import com.example.demo2.bean.Cat;
import com.example.demo2.service.CatService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

@RestController
public class CatController {

    @Resource
    private CatService catService;

    @RequestMapping("/save")
    public void save(String name, int age){
        Cat cat = new Cat();
        cat.setCatName(name);
        cat.setCatAge(age);
        catService.save(cat);
    }

    @RequestMapping("/delete")
    public void delete(int id){
        catService.delete(id);
    }

    @RequestMapping("/findAll")
    public Iterable<Cat> findAll(){
        return catService.findAll();
    }

    @RequestMapping("/findPage")
    public Iterable<Cat> findPage(int page, int size){
        return catService.findPage(page, size);
    }

    @RequestMapping("/update")
    public void update(int id, String name, int age){
        catService.update(id, name, age);
    }

    @RequestMapping("/findOne")
    public Iterable<Cat> findOne(int id){
        List<Cat> oneCat = new ArrayList();
        oneCat.add(catService.findOne(id));
        return oneCat;
    }

}
