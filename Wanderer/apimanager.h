#ifndef APIMANAGER_H
#define APIMANAGER_H

#include <QObject>
#include <QNetworkAccessManager>

class ApiManager : public QObject
{
    Q_OBJECT

public:
    explicit ApiManager(QObject *parent = nullptr);
    ~ApiManager();
public slots:
   Q_INVOKABLE void loginUser(const QString& login, const QString& password);
   Q_INVOKABLE void registerUser(const QString &login, const QString &password, const QString& passwordRepeated, const QString& emailAddress);
   Q_INVOKABLE void logoutUser();
signals:
   void loginCorrect(const QString& token);
   void loginFailed();
   void registerCorrect();
   void registerFailed();
   void logoutCorrect();
   void logoutFailed();

private:
    QNetworkAccessManager* networkManager;
    QString m_token;

    QByteArray prepareLoginData(const QString &login, const QString &password);
    QByteArray prepareRegisterData(const QString &login, const QString &password, const QString& passwordRepeated, const QString& emailAddress);
    void handleLoginResponse(QNetworkReply *reply);
    void handleRegisterResponse(QNetworkReply *reply);
    void handleLogoutResponse(QNetworkReply *reply);
};


#endif // APIMANAGER_H
