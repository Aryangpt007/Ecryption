#include <iostream>
#include <stdlib.h>
#include <string.h>

using namespace std;

string globtree = "";

FILE *fl1, *fl2, *fkey, *dfl1, *dfl2, *dfl;

string k;

class node  
{  
    public: 
    char data;  
    node* left;  
    node* right;  
};  

class node1		//declaring node class which will store the data
{
	public:
		node *dat;
		node1 *next;
};

node* newNode(char data)  
{  
    node* Node = new node(); 
    Node->data = data;  
    Node->left = NULL;  
    Node->right = NULL;  
  
    return (Node);  
}  

void printGivenLevel(node* root, int level);  
int height(node* node);  
node* newNode(int data);  
  
/* Function to print level  
order traversal a tree*/
void printLevelOrder(node* root)  
{  
    int h = height(root);  
    int i;  
    for (i = 1; i <= h; i++)  
        printGivenLevel(root, i);  
}  
  
/* Print nodes at a given level */
void printGivenLevel(node* root, int level)  
{  
	//cout << "__" << globtree << "__";
    if (root == NULL)  
        return;  
    if (level == 1)  
        globtree = globtree + root->data;  
    else if (level > 1)  
    {  
        printGivenLevel(root->left, level-1);  
        printGivenLevel(root->right, level-1);  
    }  
}  
  
/* Compute the "height" of a tree -- the number of  
    nodes along the longest path from the root node  
    down to the farthest leaf node.*/
int height(node* node)  
{  
    if (node == NULL)  
        return 0;  
    else
    {  
        /* compute the height of each subtree */
        int lheight = height(node->left);  
        int rheight = height(node->right);  
  
        /* use the larger one */
        if (lheight > rheight)  
            return(lheight + 1);  
        else return(rheight + 1);  
    }  
}  

class List : public node1		//inheriting node class in List. List will contain all the methods
{
	public:
		node1 *listptr,*temp;
	
		List()					//contructor to initialize node pointers to NULL
		{
			listptr = NULL;
			temp = NULL;
		}
			
		
		void push(node *num)	//this method inserts an element at the end of the list
		{
			node1 *newnode = new node1;
			
			newnode->dat = num;
			newnode->next = NULL;
			
			if(listptr == NULL)
			{
				listptr = newnode;
				temp = newnode;
			}
			else
			{
				temp->next = newnode;
				temp = newnode;
			}
		}
		
		
		node* pop()	//this method deletes element from the end of the list
		{
			node *num;
			
			node1 *temp1;
			
			if(listptr == NULL)
			{
				cout << "The stack is empty";
			}
			else if(listptr == temp)
			{
				num = temp->dat;
				
				delete temp;
				listptr = NULL;
				temp = NULL;
				
				return num;
			}
			else
			{
				for(temp1 = listptr; (temp1->next)->next; temp1 = temp1->next);		//traversing to one before the last element
			
				num = temp->dat;
			
				delete temp;
				temp = temp1;
				temp->next = NULL;
				
				return num;
			}
		}
		
};

string inorder(node *root)
{
	string txt = "";
	node *temp2;
	temp2 = root;
	List stack;
	
	while(1)
	{
		while(temp2)
		{
			stack.push(temp2);
			temp2 = temp2->left;
		}
		if(stack.listptr == NULL)
		{
			break;
		}
		
 		temp2 = stack.pop();
		txt = txt + temp2->data;
		temp2 = temp2->right;
	}
	
	return txt;
}
		
string preorder(node *root)
{
	string key;
	node *temp2;
	temp2 = root;
	List stack;
	
	while(1)
	{
		while(temp2)
		{
			key = key + temp2->data;
			stack.push(temp2);
			temp2 = temp2->left;
		}
		
		if(stack.listptr == NULL)
		{
			break;
		}
					
		temp2 = stack.pop();
		temp2 = temp2->right;				
	}
	
	return key;
}

void storeAlternate(node *root, char arr[], int *index, int l) 
{ 
    // Base case 
    if (root == NULL) return; 
  
    // Store elements of left subtree 
    storeAlternate(root->left, arr, index, l+1); 
  
    // Store this node only if this is a odd level node 
    if (l%2 != 0) 
    { 
        arr[*index] = root->data; 
        (*index)++; 
    } 
  
    // Store elements of right subtree 
    storeAlternate(root->right, arr, index, l+1); 
} 

void modifyTree(node *root, char arr[], int *index, int l) 
{ 
    // Base case 
    if (root == NULL) return; 
  
    // Update nodes in left subtree 
    modifyTree(root->left, arr, index, l+1); 
  
    // Update this node only if this is an odd level node 
    if (l%2 != 0) 
    { 
        root->data = arr[*index]; 
        (*index)++; 
    } 
  
    // Update nodes in right subtree 
    modifyTree(root->right, arr, index, l+1); 
} 

void reverse(char arr[], int n) 
{ 
    int l = 0, r = n-1; 
    while (l < r) 
    { 
        int temp = arr[l]; 
        arr[l] = arr[r]; 
        arr[r] = temp; 
        l++; r--; 
    } 
} 

void reverseAlternate(node *root) 
{ 
    // Create an auxiliary array to store nodes of alternate levels 
    char *arr = new char[100]; 
    int index = 0; 
  
    // First store nodes of alternate levels 
    storeAlternate(root, arr, &index, 0); 
  
    // Reverse the array 
    reverse(arr, index); 
  
    // Update tree by taking elements from array 
    index = 0; 
    modifyTree(root, arr, &index, 0); 
} 

int search(char arr[], int strt, int end, char value)  
{  
    int i;  
    for (i = strt; i <= end; i++)  
    {  
        if (arr[i] == value)  
            return i;  
    }  
}  

node* buildTree(char in[], char pre[], int inStrt, int inEnd,int n)  
{  
    
  
    if (inStrt > inEnd)  
        return NULL;  
  
    /* Pick current node from Preorder 
    traversal using preIndex  
    and increment preIndex */
    node* tNode = newNode(pre[n++]);  
  
    /* If this node has no children then return */
    if (inStrt == inEnd)  
        return tNode;  
  
    /* Else find the index of this node in Inorder traversal */
    int inIndex = search(in, inStrt, inEnd, tNode->data);  
  
    /* Using index in Inorder traversal, construct left and  
    right subtress */
    tNode->left = buildTree(in, pre, inStrt, inIndex - 1,n);  
    tNode->right = buildTree(in, pre, inIndex + 1, inEnd,n);  
  
    return tNode;  
}  



node* insertLevelOrder(char arr[], node* root, 
                       int i, int n) 
{ 
    // Base case for recursion 
    if (i < n) 
    { 
        node* temp = newNode(arr[i]); 
        root = temp; 
  
        // insert left child 
        root->left = insertLevelOrder(arr, root->left, 2 * i + 1, n); 
  
        // insert right child 
        root->right = insertLevelOrder(arr, root->right, 2 * i + 2, n); 
    } 
    return root; 
} 

string First_lvl(string s)
{
	int strlen = s.size();
	
	int asci[strlen];
	int pos[strlen];

	
	for(int i = 0; i < strlen; i++)
	{
		asci[i] = (int)s[i] - NULL;
		//cout << s[i] << " " << asci[i] << " ";
 	}
 	
 	for(int i = 0; i < strlen; i++)
	{
		pos[i] = i+1;
 	}
 	
 	for(int i = 0; i < strlen; i = i + 2)
 	{
 		int temp;
 		temp = pos[i];
 		pos[i] = pos[i+1];
 		pos[i+1] = temp;
	}
	
	int final_asci[strlen];
	
	for(int i = 0; i < strlen; i++)
	{
		final_asci[i] = asci[i] + pos[i];
	}
	
	s = "";
	
	for(int i = 0; i < strlen; i++)
	{
		s = s + (char)final_asci[i];
 	}
 	
 	return s;
}

string Second_lvl(string s)
{
	int strlen = s.size();
	
	char arr[strlen];
	
	for (int i = 0; i < strlen; i++)
	{
		arr[i] = s[i];
	}
	
	node* root = insertLevelOrder(arr,root,0,strlen);
	
	reverseAlternate(root);
	
	string txt = inorder(root);
	
	string key = preorder(root);
	
	
	const char *c2 = key.c_str();
	
	key = key + " ";
	
	const char *key1 = key.c_str();
    fputs(key1, fkey);
	
	k = key;
		
	return txt;
}

string First_lvld(char ino[], char pro[],int l)
{
	node *root = buildTree(ino,pro,0,l-1,0);
	
	reverseAlternate(root);
	
	printLevelOrder(root);
	
	string s = globtree;
	//cout << globtree << "****";
	globtree = "";
	return s;
}

string Second_lvld(string s)
{
	int strlen = s.size();
	
	int asci[strlen];
	int pos[strlen];

	
	for(int i = 0; i < strlen; i++)
	{
		asci[i] = (int)s[i];
 	}
 	
 	for(int i = 0; i < strlen; i++)
	{
		pos[i] = i+1;
 	}
 	
 	for(int i = 0; i < strlen; i = i + 2)
 	{
 		int temp;
 		temp = pos[i];
 		pos[i] = pos[i+1];
 		pos[i+1] = temp;
	}
	
	int final_asci[strlen];
	
	for(int i = 0; i < strlen; i++)
	{
		final_asci[i] = asci[i] - pos[i];
	}
	
	s = "";
	
	if(final_asci[strlen-1] == 32)
	{
		for(int i = 0; i < strlen-1; i++)
		{
			s = s + (char)final_asci[i];
 		}
 	}
 	else
 	{
 		for(int i = 0; i < strlen; i++)
		{
			s = s + (char)final_asci[i];
 		}
	}
	return s;
}

string encrypt(string s)
{
	if(s.length() % 2 != 0)
	{
		//cout << "space";
		s = s + " ";
	} 
	s = First_lvl(s);
	s = Second_lvl(s);
	
	return s;
}

string decrypt(string key,string txt)
{
	int strlen1 = key.size();
	int strlen2 = txt.size();
	
	char ino[strlen2];
	char pro[strlen1];
	
	for (int i = 0; i < strlen1; i++)
	{
		pro[i] = key[i];
	}
	
	for (int i = 0; i < strlen2; i++)
	{
		ino[i] = txt[i];
	}
	
	
	string s = First_lvld(ino,pro,strlen1);
	s = Second_lvld(s);
	
	return s;
}


void enc_file(const char *dir)
{
	fl1 = fopen(dir,"r");
//	cout << "f open";
	
	
	string c;
	
	for (int i=0; i < sizeof(dir) ; i++)
	{
		if(dir[i] == '.')
		{
			c = c + "_enc";
			c = c + dir[i];
		}
		else
		{
			c = c + dir[i];
		}
	}
	
	//cout << c;
	
	const char *c1 = c.c_str();
	char s[1000];
	
	fl2 = fopen(c1,"w+");
	
	fclose(fopen("key.txt", "w"));
	fkey = fopen("key.txt","w");
	
	while(!feof(fl1))
    {
        char a = ' ';
        
        string enc = "";
        
        while(a != EOF)
        {
        	a = fgetc(fl1);
        	cout << a << " ";
        	if(a == ' ')
        	{
        		enc = encrypt(enc);
        		enc = enc + " ";
        		const char *enc1 = enc.c_str();
        		fputs(enc1, fl2);
        		enc = "";
			}
			else if(a != EOF)
			{
				enc = enc + a;
			}
			
		}
		cout << enc;
		enc = encrypt(enc);
		cout << enc;
        const char *enc1 = enc.c_str();
        fputs(enc1, fl2);
        enc = "";
        
        
    }
    fclose(fl1);
    fclose(fl2);
    fclose(fkey);
}


dec_file(const char *dir,const char *key)
{
	dfl1 = fopen(dir,"r");
	dfl2 = fopen(key,"r");
	dfl = fopen("Converted_file.txt","w");
	
	
	while(!feof(dfl1))
    {
        char a = ' ';
        char b = ' ';
        string enc = "";
        string keys = "";
        string anss = "";
        
        while(a != EOF)
        { 
        	a = fgetc(dfl1);
        	b = fgetc(dfl2);
        	cout << b << a << " ";
        	if(a == ' ')
        	{
        		cout << enc << keys << " ------- ";
        		anss = decrypt(keys,enc);
        		anss = anss + " ";
        		cout << anss << " ....... ";
        		const char *enc1 = anss.c_str();
        		fputs(enc1, dfl);
        		
        		anss = "";
        		enc = "";
        		keys = "";
			}
			else
			{
				enc = enc + a;
				keys = keys + b;
			}
			
		}
		anss = decrypt(keys,enc);
        const char *enc1 = anss.c_str();
        fputs(enc1, dfl);
        anss = "";
        enc = "";
        keys = "";
    }
    fclose(dfl1);
    fclose(dfl2);
    fclose(dfl);
}


main()
{
	menu:
	
	//system("cls");
	
	cout << "\t\t\t\tENCRYPTION PROGRAM\n";
	
	cout << "Enter the choice:\n1. Encrypt\n2. Decrypt\n3. Exit";
	
	int ch;
	
	cin >> ch;
	
	switch(ch)
	{
		case 1:
			{
				cout << "Enter the choice:\n1. Encrypt Text\n2. Encrypt File\n";
				int ch1;
				cin >> ch1;
				
				switch(ch1)
				{
					case 1:
						{
							cout << "Enter the string to encrypt: \n";
	
							string str;
							getline(cin,str);
							getline (cin,str);
				
							if(str.size() % 2 != 0)
							{
								str = str + " ";
							}
	
							string ans = encrypt(str);
	
							cout << "\nThe Encrypted text is: " << ans;	
							cout << "\nThe Encryption key is: " << k;
						}
						break;
						
					case 2:
						{
							cout << "Enter the directory of file to encrypt";
							string f_dir;
							getline (cin,f_dir);
							getline (cin,f_dir);
							
							const char* fdir = f_dir.c_str();
							
							//cout << fdir;
							
							enc_file(fdir);
						}
					
				}
			}
			break;
		case 2:
			{
				
				cout << "Enter the choice:\n1. Decrypt Text\n2. Decrypt File\n";
				int ch1;
				cin >> ch1;
				
				switch(ch1)
				{
					case 1:
						{
							string key, txt;
	
							cout << "\nEnter the Encrypted text: ";
							getline(cin,txt);
							getline(cin,txt);
	
							cout << "\nEnter the Encryption key: ";
							getline(cin,key);
		
							string ans1 = decrypt(key,txt);
		
							cout << "\nThe text is: " << ans1;
						}
						
						break;
						
					case 2:
						{
							cout << "Enter the directory of file to Decrypt";
							string f_dir;
							getline (cin,f_dir);
							getline (cin,f_dir);
							
							const char* fdir = f_dir.c_str();
							
							//cout << fdir;
							
							cout << "Enter the directory of key";
							string f_dirk;
							getline (cin,f_dirk);
							
							const char* fdirk = f_dirk.c_str();
							
							dec_file(fdir,fdirk);
						}
					
				}
				
			}
			break;
			
		case 3:
			exit(0);
			break;
			
		default:
			goto menu;	
	}
	
	goto menu;
	
}
