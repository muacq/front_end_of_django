package com.example.demo2.repository;

import com.example.demo2.bean.Cat;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.data.repository.query.Param;

public interface CatRepository extends PagingAndSortingRepository<Cat, Integer> {
    @Query("select c from Cat c where catName=:cn")
    public Cat findMyCatName(@Param("cn") String catName);

    @Modifying
    @Query("update Cat c set c.catName=:cn, c.catAge=:age where c.id=:id")
    public void update(@Param("id")int id, @Param("cn")String catName, @Param("age")int catAge);
}
