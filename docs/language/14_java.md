---
title: java
layout: default
parent: Language
nav_order: 12
permalink: /language/java
# nav_exclude: true
# search_exclude: true
---

# 0. 환경설정

## 1. intelliJ 설치 및 설정
- intelliJ Ultimate(30일 무료평가판)이나 Community Edition을 설치
![](/assets/img/java/java001.png)

- 6개월 무료 쿠폰 등록(Ultimate)하려면 받은 쿠폰파일의 링크를 클릭한다.
![](/assets/img/java/java002.png)

- 쿠폰 코드 및 개인 정보 입력하고, 제품은 IntelliJ IDEA Ultimate 를 선택하고 Redeem 버튼을 클릭하고 로그인 등 등록 작업을 진행한다.
![](/assets/img/java/java003.png)

- 등록된 라이센스를 확인한다.
![](/assets/img/java/java004.png)


## java  프로그램 최종 테스트 코드
Customer.java
```java
package customer;
/* * 요구사항 정의
 * 1. 고객 정보는 이름, 성별, 이메일, 출생 연도로 구성되어 있음
 * - 이름 : 문자열
 * - 성별 : 'M','F'
 * - 이메일 : 문자열
 * - 출생연도 : 정수*/
public class Customer {
//    고객정보를 저장하는 인스턴스 변수 선언
    private String name;
    private char gender;
    private String email;
    private int birthYear;

//    고객 생성시 생성자를 이용해서 생성
    Customer(String name, char gender, String email, int birthYear){
        this.name = name;
        this.gender = gender;
        this.email = email;
        this.birthYear = birthYear;
    }
    Customer(){}

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public char getGender() {
        return gender;
    }

    public void setGender(char gender) {
        this.gender = gender;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public int getBirthYear() {
        return birthYear;
    }

    public void setBirthYear(int birthYear) {
        this.birthYear = birthYear;
    }
}

```

CustomerManager.java

```java
package customer;

import java.util.Scanner;

/** 고객관리 프로그램의 기능
 * - 'I'를 입력하여 고객 정보 입력
 * - 저장된 고객 정보는 'P' 또는 'N'을 입력하여 이전 또는 다음 고객정보를 조회할 수 있음
 * - 'C'를 입력하면 현재 인덱스의 고객 정보를 조회할 수 있음
 * - 조회한 고객 정보를 'U'를 입력하여 수정할 수 있음.
 * - 'D'를 입력하면 조회한 고객 정보를 배열에서 삭제
 * - 프로그램을 종료하려면 'Q'를 입력*/
public class CustomerManager {
    // 배열에 저장할 수 있는 최대 고객 수 100
    static final int MAX = 100;
    // 고객 정보를 저장할수 있는 변수를 배열로 선언
    static Customer[] customers = new Customer[MAX];
    // 배열에 접근할 인덱스
    static int index = 2;
    //현재 데이터가 몇개 저장되어 있는지 알수 있는 변수
    static int count = 3;
    // 터미널에서 표준 입력장치로 데이터를 입력받기 위한 Scanner 객체 생성
    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        customers[0] = new Customer("hong",'m',"hong@gmail.com",2000);
        customers[1] = new Customer("kim",'f',"kim@gmail.com",2010);
        customers[2] = new Customer("lee",'m',"lee@gmail.com",2005);
        while(true){
            System.out.printf("\n[INFO] 고객수 : %d, 인덱스 : %d\n",count,index);
            System.out.println("메뉴를 입력하세요");
            System.out.println("(I)nput, (P)revious, (N)ext, (C)urrent, (U)pdate, (D)elete, (Q)uit");
            System.out.print("메뉴 입력 : ");
            String menu = scanner.next();
            menu = menu.toUpperCase();
            switch (menu){
                case "I":
                    System.out.println("고객정보를 입력합니다.");
                    if(count >= MAX){
                        System.out.println("데이터를 더 이상 추가할 수 없습니다.");
                    }else{
                        insertCustomer();
                        System.out.println("고객 정보를 저장했습니다.");
                    }
                    break;
                case "P":
                    System.out.println("이전 데이터를 출력합니다.");
                    if(index <= 0){
                        System.out.println("이전 데이터가 존재하지 않습니다.");
                    }else{
                        index--;
                        printCustomer();
                    }
                    break;
                case "N":
                    System.out.println("다음 데이터를 출력합니다.");
                    if(index >= count-1){
                        System.out.println("다음 데이터가 존재하지 않습니다.");
                    }else {
                        index++;
                        printCustomer();
                    }
                    break;
                case "C":
                    System.out.println("현재 데이터를 출력합니다.");
                    if((index >= 0 && index < count)){
                        printCustomer();
                    }else{
                        System.out.println("데이터가 없습니다.");
                    }
                    break;
                case "U":
                    System.out.println("데이터를 수정합니다.");
                    if((index >= 0) && (index < count)){
                        System.out.println(index+1+"번째 데이터를 수정합니다.");
                        updateCustomer();
                    }else{
                        System.out.println("데이터가 선택되지 않았습니다.");
                    }
                    break;
                case "D":
                    System.out.println("데이터를 삭제합니다.");
                    if((index >= 0) && (index < count)){
                        System.out.println(index+1+"번째 데이터를 삭제합니다.");
                        deleteCustomer();
                    }else{
                        System.out.println("데이터가 선택되지 않았습니다.");
                    }
                    break;
                case "Q":
                    System.out.println("프로그램을 종료합니다.");
                    scanner.close();
                    System.exit(0);
                    break;
                default:
                    System.out.println("메뉴를 잘못 입력하셨습니다.");
            }
        }
    }

    public static void insertCustomer(){
        System.out.print("이름 : ");
        String name = scanner.next();
        System.out.print("성별(M/F) : ");
        char gender = scanner.next().charAt(0);
        System.out.print("이메일 : ");
        String email = scanner.next();
        System.out.print("출생연도 : ");
        int birthYear = scanner.nextInt();
        customers[count] = new Customer(name,gender,email,birthYear);
        count++;
        index++;

    }

    public static void printCustomer(){
        System.out.println("================== Customer Info ===============");
        Customer customer = customers[index];
        System.out.println("이름 : "+customer.getName());
        System.out.println("성별 : "+customer.getGender());
        System.out.println("이메일 : "+customer.getEmail());
        System.out.println("출생연도 : "+customer.getBirthYear());
        System.out.println("=================================================");
    }

    public static void updateCustomer(){
        Customer customer = customers[index];
        System.out.println("================ Update Customer Info ===============");
        System.out.print("이름("+customer.getName()+") : ");
        customer.setName(scanner.next());
        System.out.print("성별("+customer.getGender()+") : ");
        customer.setGender(scanner.next().charAt(0));
        System.out.print("이메일("+customer.getEmail()+") : ");
        customer.setEmail(scanner.next());
        System.out.print("출생연도("+customer.getBirthYear()+") : ");
        customer.setBirthYear(scanner.nextInt());

    }

    public static void deleteCustomer(){
        for(int i = index; i < count-1; i++){
            customers[i] = customers[i+1];
        }
        count--;
    }

}

```
