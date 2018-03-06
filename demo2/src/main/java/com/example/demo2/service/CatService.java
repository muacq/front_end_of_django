package com.example.demo2.service;

import com.example.demo2.bean.Cat;
import com.example.demo2.repository.CatRepository;
import org.springframework.core.convert.converter.Converter;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.data.domain.Sort.Order;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import javax.transaction.Transactional;
import java.util.Iterator;
import java.util.List;

@Service
public class CatService {

    @Resource
    private CatRepository catRepository;

    @Transactional
    public void save(Cat cat){
        catRepository.save(cat);
    }

    @Transactional
    public void delete(int id){
        catRepository.delete(id);
    }

    public Iterable<Cat> findAll(){
        return catRepository.findAll();
    }

    public Iterable<Cat> findPage(int currentPage, int pageSize){
        Order idOrder = new Order(Direction.ASC, "id");
        Order nameOrder = new Order(Direction.ASC, "catName");
        Sort sort = new Sort(idOrder, nameOrder);
        PageRequest pageRequest = new PageRequest(currentPage - 1, pageSize, sort);
        Page<Cat> page = catRepository.findAll(pageRequest);
        return page;
    }

    @Transactional
    public void update(int id, String name, int age){
        catRepository.update(id, name, age);
    }

    public Cat findOne(int id){
        return catRepository.findOne(id);
    }
}
