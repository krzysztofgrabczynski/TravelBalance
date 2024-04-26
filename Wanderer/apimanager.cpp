#include "apimanager.h"
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonObject>
#include <QJsonDocument>
#include <QDebug>
#include <QFile>
#include <QJsonArray>

ApiManager::ApiManager(QObject *parent)
    : QObject(parent), networkManager(new QNetworkAccessManager)
{
}

ApiManager::~ApiManager()
{
    delete networkManager;
}

static const QString apiAdressLogin = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/login/";
static const QString apiAddresLogout = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/logout/";
static const QString apiAddresRegister = "https://wanderer-test-fe529f1fdf47.herokuapp.com/api/user/";

QByteArray ApiManager::prepareLoginData(const QString &login, const QString &password)
{
    QJsonObject jsonObject;
    jsonObject["username"] = login;
    jsonObject["password"] = password;
    return QJsonDocument(jsonObject).toJson();
}

QByteArray ApiManager::prepareRegisterData(const QString &login, const QString &password, const QString& passwordRepeated, const QString& emailAddress)
{
    QJsonObject jsonObject;
    jsonObject["username"] = login;
    jsonObject["password"] = password;
    jsonObject["password2"] = passwordRepeated;
    jsonObject["email"] = emailAddress;
    return QJsonDocument(jsonObject).toJson();
}


void ApiManager::loginUser(const QString &login, const QString &password)
{
    QNetworkRequest request{QUrl(apiAdressLogin)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareLoginData(login, password);
    QNetworkReply *reply = networkManager->post(request, requestData);

    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleLoginResponse(reply);
        reply->deleteLater();
    });
}

void ApiManager::handleLoginResponse(QNetworkReply *reply)
{
    if (reply->error() == QNetworkReply::NoError) {
        QByteArray responseData = reply->readAll();
        qDebug(responseData);
        QJsonDocument jsonDocument = QJsonDocument::fromJson(responseData);
        QJsonObject jsonObject = jsonDocument.object();

        if (jsonObject.contains("token")) {
            m_token = jsonObject["token"].toString();
            emit loginCorrect(m_token);
        } else {
            qDebug() << "Token not found in JSON response.";
            emit loginFailed();
        }

        if(jsonObject.contains("status")){
            qDebug() << "Status: " << jsonObject["status"].toInt();
        }else{
            qDebug() << "Status not found in JSON response.";
        }

    } else {
        qDebug() << "Error:" << reply->errorString();
        emit loginFailed();
    }
}

void ApiManager::registerUser(const QString &login, const QString &password, const QString& passwordRepeated, const QString& emailAddress)
{
    QNetworkRequest request{QUrl(apiAddresRegister)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QByteArray requestData = prepareRegisterData(login, password, passwordRepeated, emailAddress);

    QNetworkReply *reply = networkManager->post(request, requestData);
    connect(reply, &QNetworkReply::finished, [=]() mutable {
        handleRegisterResponse(reply);
        reply->deleteLater();
    });

}

void ApiManager::handleRegisterResponse(QNetworkReply *reply){
    if (reply->error() == QNetworkReply::NoError) {
        qDebug() << "Response:" << reply->readAll();
        emit registerCorrect();
    } else {
        qDebug() << "Error:" << reply->errorString();
        emit registerFailed();
    }
}

void ApiManager::logoutUser()
{
    if(m_token.isEmpty())
    {
        emit logoutFailed();
        return;
    }

    QNetworkRequest request{QUrl(apiAddresLogout)};
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    request.setRawHeader("Authorization", QByteArray("Token ").append(m_token.toUtf8()));
    QNetworkReply *reply = networkManager->post(request, QByteArray());

    connect(reply, &QNetworkReply::finished, [=]() {

        reply->deleteLater();
    });
}

void ApiManager::handleLogoutResponse(QNetworkReply *reply)
{
    if (reply->error() == QNetworkReply::NoError) {
        QByteArray responseData = reply->readAll();
        qDebug() << responseData;
        this->m_token.clear();
        emit logoutCorrect();
    } else {
        qDebug() << "Error:" << reply->errorString();
        emit logoutFailed();
    }
}



