#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<map>
#include<ctime>
using namespace std;

struct compromissos{
    string nome_compromisso, data_compromisso, hora_compromisso;
    int estado_compromissso=0;
};

map <string,compromissos> numero_telefone;

bool validar_data(string data){
    stringstream ss (data);//fatiamento de string
    string dia_str, mes_str, ano_str;//variaveis para receber D/M/A
    
    getline(ss,dia_str,'/');
    getline(ss,mes_str,'/');//separa pela barra e insere na variavel
    getline(ss,ano_str,'/');
  
    if(dia_str.empty() || mes_str.empty() || ano_str.empty()) return false;

    int dia= stoi(dia_str);
    int mes= stoi(mes_str);
    int ano= stoi(ano_str);

    if(dia>= 1 && dia <=31 && mes >=1 && mes <=12 && ano>=2026){
        return true;
    }
    return false;
}

bool validar_hora(string hora){
    stringstream rr(hora);
    string hora_str, min_str;

    getline(rr,hora_str,':');
    getline(rr,min_str,':');

    if(hora_str.empty() || min_str.empty()) return false;

    int hora_int = stoi(hora_str);
    int minutos_int = stoi(min_str);

    if(hora_int<=23 && hora_int >=0 && minutos_int<=59 && minutos_int>=0){
        return true;
    }

    return false;
}


void processar_mensagem (string telefone, string mensagem){
    
    int estado_processamento= numero_telefone[telefone].estado_compromissso;
        
    switch(estado_processamento){
        
        case 1:{
            numero_telefone[telefone].nome_compromisso=mensagem;
            cout << "***Compromisso salvo***\n";
            if(numero_telefone[telefone].estado_compromissso==1){
                cout<<"informe a data separadas dessa forma 'DD/MM/AAAA': ";
            }
            numero_telefone[telefone].estado_compromissso++;
            cout<<endl;
            break;
        }

        case 2:{
            if(validar_data(mensagem)){
               numero_telefone[telefone].data_compromisso=mensagem;
                cout << "***Data salva***\n";
                if(numero_telefone[telefone].estado_compromissso==2){
                    cout<<"Agora informe a hora nesse formato'00:00':";
                }
                numero_telefone[telefone].estado_compromissso++;
                break; 
            }
            else{
                cout<<"Data invalida!!!\n  Vamos tentar novamente";
                break;
            }
        }

        case 3:{
            if(validar_hora(mensagem)){
                numero_telefone[telefone].hora_compromisso=mensagem;

                ofstream salva_chatbot("dados_compromisso.txt",ios::app);

                if(!salva_chatbot.is_open()){
                    cout<<"Erro ao abrir arquivo\n";
                    return;
                }

                salva_chatbot<<telefone<<","
                <<numero_telefone[telefone].nome_compromisso<<","
                <<numero_telefone[telefone].data_compromisso<<","
                <<numero_telefone[telefone].hora_compromisso<<",0"<<endl;

                salva_chatbot.close();
                numero_telefone[telefone].estado_compromissso=0;
                estado_processamento=0;
                break;
            }  
            else{
                cout<<"Hora invalida, lembre-se de usar formato 00:00";
                break;
            }          
        }
    }        
}

time_t converter(string data, string hora) {
    int d, m, a, h, min;
    char sep;

    stringstream sd(data);
    sd >> d >> sep >> m >> sep >> a;

    stringstream sh(hora);
    sh >> h >> sep >> min;

    tm t = {};
    t.tm_mday = d;
    t.tm_mon = m - 1;
    t.tm_year = a - 1900;
    t.tm_hour = h;
    t.tm_min = min;
    t.tm_sec = 0;

    return mktime(&t);
}

void verificar_alertas(){
    ifstream arquivo("dados_compromisso.txt");
    string linha;
    time_t agora = time(0);

    while(getline(arquivo, linha)){
        stringstream ss(linha);
        string telefone, nome, data, hora, concluido;

        getline(ss, telefone, ',');
        getline(ss, nome, ',');
        getline(ss, data, ',');
        getline(ss, hora, ',');
        getline(ss, concluido, ',');

        if(concluido == "1") continue; 

        try{
            time_t tempo_compromisso = converter(data, hora);
            double diff = difftime(tempo_compromisso, agora);
            
            if(diff <= 60 && diff > -60){
                cout << "\n*** LEMBRETE ***\n";
                cout << "Telefone: " << telefone << "\n";
                cout << "Compromisso: " << nome << "\n";
                cout << "Data: " << data << " Hora: " << hora << "\n";
            }
        } 
        catch(...){
            continue;
        }
    }
}

int main(){

int adiciona_compromisso=1;
string mensagem_zap,telefone_zap;

cout<<"Digite seu telefone";
cin>>telefone_zap;

cout<<"Vou lhe ajudar a lembrar seus compromissos.\n";
numero_telefone[telefone_zap].estado_compromissso=1;

while(adiciona_compromisso!=0){
    
    verificar_alertas();
    if(numero_telefone[telefone_zap].estado_compromissso==1){
    cout<<"Digite o titulo desse lembrete?   ";}
    if(numero_telefone[telefone_zap].estado_compromissso==2){
    cout<<" Informe a data 'DD/MM/AAAA': "; 
    }
    if(numero_telefone[telefone_zap].estado_compromissso==3){
    cout<<" Informe a hora 'HH:MM': "; 
    }
    
    
    cin>>mensagem_zap;

    if(adiciona_compromisso==1){
        processar_mensagem(telefone_zap,mensagem_zap);
    }

    if(numero_telefone[telefone_zap].estado_compromissso==0){
    cout<<"Deseja se lembrar de mais alguma coisa?\n-1 para adicionar lembrete\n-0 para sair. ";
    cin>>adiciona_compromisso;

        if(adiciona_compromisso==0){
            cout<<"Agradecemos o contato";
        }
    }
}
}



