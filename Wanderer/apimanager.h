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
   Q_INVOKABLE void registerUser(const QString &login, const QString &password);
   Q_INVOKABLE void logoutUser();
signals:
   Q_INVOKABLE void loginCorrect(const QString& token);
   Q_INVOKABLE void loginFailed();
   Q_INVOKABLE void registerCorrect();
   Q_INVOKABLE void registerFailed();
   Q_INVOKABLE void logoutCorrect();
   Q_INVOKABLE void logoutFailed();

private:
    QNetworkAccessManager* networkManager;
    QString m_token;

    QByteArray prepareUserData(const QString &login, const QString &password);
    void handleLoginResponse(QNetworkReply *reply);
    void handleRegisterResponse(QNetworkReply *reply);
    void handleLogoutResponse(QNetworkReply *reply);
};


#endif // APIMANAGER_H
