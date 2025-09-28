CREATE DATABASE cleaning;

use cleaning;

SELECT * FROM laptops
WHERE TypeName LIKE'%book' ;


SELECT * FROM laptops
WHERE TypeName LIKE'book%';

SELECT * FROM laptops
WHERE TypeName LIKE'%book%';

SELECT TypeName , LOWER(TypeName) , UPPER(TypeName)
FROM laptops;

SELECT * FROM laptops;
   
SELECT CONCAT(Company  , " ", TypeName)
-- on string only 
FROM laptops; 

SELECT CONCAT_WS("-",Company  , ScreenResolution , TypeName)
-- on string only 
FROM laptops; 

SELECT TypeName , SUBSTR(TypeName , 1 , 5 )
-- substring from 1 to 5 and starting index is always 1 
FROM laptops;

SELECT TypeName , SUBSTR(TypeName , 1  )
-- substring from 1 to end and starting index is always 1 
FROM laptops;

SELECT TypeName , SUBSTR(TypeName , -1  )
-- substring of-1  and starting index is always 1 
FROM laptops;

SELECT TypeName , SUBSTR(TypeName , -5 , 2  )
-- substring from -5 se two charachter  and starting index is always 1 
FROM laptops;


SELECT REPLACE("ULTRABOOK" , "BOOK" , "PAD")
-- REplace the string ultrabook of BOOK with PAD 
FROM laptops;

SELECT 5 + 6;

SELECT REPLACE(TypeName, "Ultrabook" , "SamsungPad")
-- REplace the string ultrabook of BOOK with PAD 
FROM laptops;


SELECT TypeName , SUBSTR(TypeName , -2  )
-- substring last two character 
FROM laptops;

SELECT TypeName, REVERSE(TypeName) 
-- REVERSE Of the string 
FROM laptops;

SELECT TypeName
-- REVERSE as Palindrome  
FROM laptops
WHERE TypeName = REVERSE(TypeName);

SELECT Gpu , LENGTH(Gpu) , CHAR_LENGTH(Gpu)
-- Total num of char in a string  
FROM laptops;

SELECT Gpu , LENGTH(Gpu) , CHAR_LENGTH(Gpu)
-- CHAR_LENGTH return length of the character 
-- while LENGTH return the length of the string in byte like - ^_cafe = 6 char 
FROM laptops
WHERE LENGTH(Gpu) !=  CHAR_LENGTH(Gpu);

SELECT INSERT(TypeName , 7 , 5 , 'hello')
-- insert at any place on 7 place add 5 word hello  
FROM laptops;

SELECT TypeName , LEFT(TypeName , 3 ) , RIGHT(TypeName , 4 ) 
-- EXTRACT from left to 3 char and RIGHT to 4 char from left 
FROM laptops;

SELECT REPEAT(Company  , 4 ) 
FROM laptops;


-- use to strip the space  
SELECT TRIM("                   mukesh            "); 

-- LEADING , TRAINLING ,BOTH means front and back side too 
SELECT TRIM( BOTH "."  FROM "................................mukesh................"); 
SELECT TRIM( LEADING "."  FROM "................................mukesh................"); 
SELECT TRIM( TRAILING "."  FROM "................................mukesh................"); 
-- but can't strip the inside the string 
SELECT TRIM( BOTH "."  FROM "................................muke.........sh................"); 

-- LTRIM , RTRIM  using to strip the space of left side or right side 
SELECT LTRIM("                   mukesh            ") , LENGTH(LTRIM("                   mukesh            ")) ; 
SELECT RTRIM("               mukesh          "),LENGTH(RTRIM("                mukesh          ")) ; 


SELECT "www.crashlar.com" , SUBSTRING_INDEX('www.crashlar.com' , "." , -1);
-- ACT as split funtion  
SELECT "www.crashlar.com" , SUBSTRING_INDEX('www.crashlar.com' , "." , -2);
SELECT "www.crashlar.com" , SUBSTRING_INDEX('www.crashlar.com' , "." , -3);

SELECT STRCMP('mumbai' , 'crashlar');
SELECT STRCMP('mumbai' , 'delhi');
-- equal than return 0 
-- less than return -1 
-- greater than return 1 
SELECT STRCMP('crashlar' , 'crashlar');

SELECT TypeName , LOCATE('b' , TypeName , 6 )
-- less than 6 than return 0 
FROM laptops;


SELECT TypeName , LOCATE('b' , TypeName  ) 
FROM laptops;

SELECT LPAD('XXXXXXXXXX' , 13 , '+91');
SELECT RPAD('XXXXXXXXXX' , 13 , '+91');
